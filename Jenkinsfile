pipeline {
    agent any

    parameters {
        string(
            name: 'GIT_BRANCH',
            defaultValue: 'main',
            description: 'Git branch to build. Use main for normal release tests.'
        )
        string(
            name: 'PYTHON_BIN',
            defaultValue: 'python3',
            description: 'Python executable used for Django checks and packaging. '
        )
        string(
            name: 'NODE_HOME_OVERRIDE',
            defaultValue: '',
            description: 'Optional Node.js home. Leave empty to use the agent default.'
        )
        string(
            name: 'RELEASE_VERSION',
            defaultValue: '',
            description: 'Optional release version, for example 0.10.0. Leave empty to use VERSION.'
        )
        booleanParam(
            name: 'PUBLISH_GITHUB_RELEASE',
            defaultValue: false,
            description: 'Publish dist assets to GitHub Releases with gh. Only use for release builds.'
        )
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
    }

    environment {
        GITHUB_REPO = 'nathabee/bench-chef'
    }

    stages {
        stage('Checkout Selected Branch') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.GIT_BRANCH ?: 'main'}"]],
                    userRemoteConfigs: [[
                        url: 'https://github.com/nathabee/bench-chef.git'
                    ]]
                ])
            }
        }

        stage('Environment') {
            steps {
                script {
                    if (params.NODE_HOME_OVERRIDE?.trim()) {
                        env.PATH = "${params.NODE_HOME_OVERRIDE.trim()}/bin:${env.PATH}"
                    }
                }

                sh '''
                    set -eu
                    echo "PATH=${PATH}"
                    which "${PYTHON_BIN}"
                    which node
                    which npm
                    which docker || true
                    which gh || true
                    "${PYTHON_BIN}" --version
                    node --version
                    npm --version
                '''
            }
        }

        stage('Resolve Version') {
            steps {
                sh '''
                    set -eu
                    RELEASE_VERSION_VALUE="${RELEASE_VERSION:-}"
                    if [ -n "${RELEASE_VERSION_VALUE}" ]; then
                      printf '%s\n' "${RELEASE_VERSION_VALUE}" > VERSION
                      tools/sync-version.sh
                    else
                      tools/check-version.sh
                    fi

                    VERSION_VALUE="$(tr -d '[:space:]' < VERSION)"
                    printf '%s\n' "${VERSION_VALUE}" > .jenkins-version
                    echo "BenchChef version: ${VERSION_VALUE}"
                '''
            }
        }

        stage('Backend Tests') {
            steps {
                sh '''
                    set -eu
                    cd backend-django
                    "${PYTHON_BIN}" -m venv .venv-ci
                    . .venv-ci/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python manage.py test
                '''
            }
        }

        stage('Frontend Build') {
            steps {
                sh '''
                    set -eu
                    cd frontend-angular
                    if [ -f package-lock.json ]; then
                      npm ci
                    else
                      npm install
                    fi
                    npm run build
                '''
            }
        }

        stage('Package Release') {
            steps {
                sh '''
                    set -eu

                    VERSION_VALUE="$(cat .jenkins-version)"
                    RELEASE_ARCHIVE="bench-chef-${VERSION_VALUE}-release.tar.gz"
                    LINUX_PACKAGE="bench-chef-${VERSION_VALUE}-linux.tar.gz"
                    WINDOWS_PACKAGE="bench-chef-${VERSION_VALUE}-windows.zip"
                    ADMIN_PACKAGE="bench-chef-${VERSION_VALUE}-admin.zip"

                    rm -rf package dist
                    mkdir -p package/linux/bench-chef package/windows/bench-chef package/admin dist

                    copy_runtime() {
                      DEST="$1"
                      mkdir -p "${DEST}"
                      cp VERSION "${DEST}/"
                      cp README.md LICENSE docker-compose.yml .env.example "${DEST}/"
                      cp -R backend-django frontend-angular/dist grafana prometheus scripts docs "${DEST}/"
                      find "${DEST}" -type d -name __pycache__ -prune -exec rm -rf {} +
                      rm -rf "${DEST}/backend-django/.venv" "${DEST}/backend-django/.venv-ci"
                      rm -f "${DEST}/backend-django/db.sqlite3" "${DEST}/backend-django/backend.log"
                    }

                    copy_runtime package/linux/bench-chef
                    copy_runtime package/windows/bench-chef

                    mkdir -p package/admin/benchchef/bin package/admin/benchchef/data package/admin/benchchef/ops
                    cp tools/win/*.ps1 package/admin/benchchef/bin/
                    cp tools/win/README.md package/admin/benchchef/bin/README.md
                    cp tools/win/run.env.example package/admin/benchchef/data/run.env.example
                    cp -R tools/ops/. package/admin/benchchef/ops/
                    cp tools/README.md package/admin/benchchef/README.md

                    tar -C package/linux -czf "dist/${LINUX_PACKAGE}" bench-chef

                    "${PYTHON_BIN}" - <<PY
import pathlib
import zipfile

for source, target, archive_root in [
    ("package/windows/bench-chef", "dist/${WINDOWS_PACKAGE}", pathlib.Path("benchchef/app")),
    ("package/admin/benchchef", "dist/${ADMIN_PACKAGE}", pathlib.Path("benchchef")),
]:
    source_path = pathlib.Path(source)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in source_path.rglob("*"):
            if path.is_file():
                zf.write(path, archive_root / path.relative_to(source_path))
PY

                    tar -C package -czf "dist/${RELEASE_ARCHIVE}" linux windows admin

                    sha256sum dist/* > dist/SHA256SUMS.txt
                    ls -lh dist
                '''

                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }

        stage('Publish GitHub Release') {
            when {
                expression {
                    return params.PUBLISH_GITHUB_RELEASE
                }
            }
            steps {
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        set -eu

                        VERSION_VALUE="$(cat .jenkins-version)"
                        TAG_NAME="v${VERSION_VALUE}"
                        TITLE="${VERSION_VALUE}"

                        API_JSON=$(mktemp)
                        cat > "${API_JSON}" <<EOF
{
  "tag_name": "${TAG_NAME}",
  "name": "${TITLE}",
  "draft": false,
  "prerelease": false,
  "generate_release_notes": true
}
EOF

                        curl -sS -X POST \
                          -H "Accept: application/vnd.github+json" \
                          -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                          "https://api.github.com/repos/${GITHUB_REPO}/releases" \
                          -d @"${API_JSON}" \
                          > github-release-response.json

                        UPLOAD_URL="$("${PYTHON_BIN}" - <<'PY'
import json

with open("github-release-response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if "upload_url" not in data:
    print("")
else:
    print(data["upload_url"].split("{")[0])
PY
)"

                        if [ -z "${UPLOAD_URL}" ]; then
                          echo "GitHub release creation did not return an upload URL." >&2
                          cat github-release-response.json >&2
                          exit 1
                        fi

                        for ARTIFACT in dist/*; do
                          CONTENT_TYPE="application/octet-stream"
                          case "${ARTIFACT}" in
                            *.tar.gz) CONTENT_TYPE="application/gzip" ;;
                            *.zip) CONTENT_TYPE="application/zip" ;;
                            *.txt) CONTENT_TYPE="text/plain" ;;
                          esac

                          ARTIFACT_NAME="$(basename "${ARTIFACT}")"
                          curl -sS -X POST \
                            -H "Accept: application/vnd.github+json" \
                            -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                            -H "Content-Type: ${CONTENT_TYPE}" \
                            "${UPLOAD_URL}?name=${ARTIFACT_NAME}" \
                            --data-binary @"${ARTIFACT}"
                        done
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'BenchChef release pipeline completed successfully.'
        }
        failure {
            echo 'BenchChef release pipeline failed. Check backend tests, frontend build, and package logs.'
        }
    }
}
