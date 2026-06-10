# Windows development setup 

> **PLEASE IGNORE THIS DOC THIS IS PRIVATE AND HAS NOTHING TODO WITH THE PROJECT**


## 1. Before installing

Use the company notebook if possible.

Check Windows type:

1. Right-click Start.
2. Click **System**.
3. Look at **System type**.
4. Usually it will be **64-bit operating system, x64-based processor**.

For downloads, choose **Windows x64** unless the laptop is clearly ARM64.

## 2. Install Visual Studio Code

1. Open the official Visual Studio Code download page.
2. Download **Windows User Installer x64**.
3. Run the installer.
4. Accept the license.
5. Keep the default installation folder.
6. Select:

   * **Add “Open with Code” action**
   * **Add to PATH**
7. Click **Install**.
8. Open VS Code.

## 3. Install VS Code extensions

In VS Code:

1. Click the **Extensions** icon on the left.
2. Search each extension by name.
3. Click **Install**.

Install these:

### Frontend

* **Angular Language Service**

  * Required version: **19.2.0**
  * After installing, check the version in the extension details.
  * If a different version is installed, use the extension gear menu and choose another version if available.

### Backend

* **C# Dev Kit**
* **C#**
* **.NET Install Tool**

Note: C# Dev Kit normally installs C# and .NET Install Tool automatically, but check that all three are present.

### Git and documentation

* **GitLens**
* **Markdown All in One**
* **markdownlint**

### AI assistant

* **Codex**

  * Requires a ChatGPT/OpenAI account.
  * Do not enter private company secrets unless the company explicitly allows it.

### Later / optional

* **Container Tools**
* **Dev Containers**

These are not urgent for the first day, but they will probably become useful later.

## 4. Install Git for Windows

1. Open the official Git for Windows download page.
2. Download the 64-bit Windows installer.
3. Run the installer.
4. Keep the default options unless the company gives another standard.
5. Important option: choose **Git from the command line and also from 3rd-party software**.
6. Finish installation.

Check installation:

Open PowerShell and run:

```powershell
git --version
```

## 5. Install ShareX

1. Open the official ShareX download page.
2. Download the Windows installer.
3. Run the installer.
4. Keep the default options.
5. Start ShareX.
6. Test one screenshot.

Useful first setting:

* Capture region
* Save screenshots automatically
* Copy image to clipboard

## 6. Install OneNote

Usually OneNote is already included with Microsoft 365 on a company notebook.

Check:

1. Open Start menu.
2. Search **OneNote**.
3. If it is missing, ask the company whether they use:

   * Microsoft Store OneNote
   * Microsoft 365 OneNote
   * Browser version

Do not install a private Microsoft account version if the company provides Microsoft 365.

## 7. Visual Studio 2022

Visual Studio 2022 is mentioned as running on the server.

For the first setup, local installation is probably not necessary unless Martin Schramm or the team asks for it.

Do not install it first unless needed, because it is large and can take time.

## 8. Install Inno Setup Compiler

1. Open the official Inno Setup page.
2. Download the current stable installer.
3. Run the installer.
4. Keep the default options.
5. Start **Inno Setup Compiler** once to verify it opens.

This tool is used to create installable Windows applications.

## 9. Optional: container tools

Only install Docker Desktop / Dev Containers if the company says you need them now.

If needed later:

1. Install Docker Desktop for Windows.
2. Enable WSL 2 integration if requested.
3. Install VS Code extension **Dev Containers**.
4. Install VS Code extension **Container Tools**.

## 10. Final check before the first appointment

Open PowerShell and check:

```powershell
git --version
code --version
```

Open VS Code and check:

* Angular Language Service installed, version 19.2.0 if available
* C# Dev Kit installed
* C# installed
* .NET Install Tool installed
* GitLens installed
* Markdown All in One installed
* markdownlint installed
* Codex installed

Also check:

* ShareX opens
* OneNote opens
* Inno Setup Compiler opens

## 11. What to ask Martin Schramm

Ask these directly during setup:

1. Which Git host is used?

   * Azure DevOps?
   * GitHub?
   * GitLab?
   * Internal server?

2. Which authentication is required?

   * Company Microsoft account?
   * SSH key?
   * Personal access token?

3. Which .NET SDK version is required?

4. Which Node.js version is required for Angular?

5. Why Angular Language Service must be exactly 19.2.0?

6. Are Docker Desktop, Dev Containers, or Container Tools already required?

7. Is Codex allowed on company source code?

8. Are screenshots with ShareX allowed for internal documentation?

## 12. Important warning

Do not install random extensions from unknown publishers.

For VS Code extensions, prefer:

* Microsoft
* Angular
* GitLens official publisher
* David Anson for markdownlint

Also do not paste company secrets, passwords, tokens, database credentials, or private source code into AI tools unless the company explicitly allows it.
