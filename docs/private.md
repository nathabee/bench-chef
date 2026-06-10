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

For the first setup, local installation is probably not necessary unless the team asks for it.

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

## 11. What to ask the developper

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



# Appendix A — Visual Studio 2022 (Optional)

## Purpose

Visual Studio 2022 is Microsoft's full Integrated Development Environment (IDE) for .NET and C# development.

It is different from Visual Studio Code:

| Tool               | Typical Usage                                                   |
| ------------------ | --------------------------------------------------------------- |
| Visual Studio Code | Angular, C#, Markdown, Git, general development                 |
| Visual Studio 2022 | Large .NET projects, advanced debugging, enterprise development |

For the repositories used by the company, Visual Studio 2022 is not necessarily required locally.

## Recommendation

Do not install Visual Studio 2022 before the first meeting unless specifically requested.

Install Visual Studio Code and the required extensions first.

Ask whether a local Visual Studio 2022 installation is needed for your role.

## Download

Official Microsoft download page:

https://visualstudio.microsoft.com/downloads/

Depending on the company license, use:

* Visual Studio Community 2022
* Visual Studio Professional 2022

Do not purchase a license yourself.

## Installation

1. Download the Visual Studio installer.
2. Run `VisualStudioSetup.exe`.
3. Wait for the Visual Studio Installer to start.

### Recommended Workload

Select:

* ASP.NET and web development

This installs:

* .NET SDK
* ASP.NET tools
* Web debugging tools
* Common C# development components

### Optional Workloads

Install only if requested:

* .NET desktop development
* Data storage and processing
* Azure development

## Verify Installation

Open PowerShell:

```powershell
dotnet --version
```

A version number should be displayed.

Example:

```text
9.0.301
```

## First Launch

Start:

```text
Visual Studio 2022
```

You may be asked to sign in with:

* a Microsoft account
* a company account

If unsure which account to use, ask the company before proceeding.

## Notes

* Installation size can range from 5 GB to more than 20 GB depending on selected workloads.
* Installation may take 20–60 minutes.
* Most day-to-day work described in the onboarding information can be performed directly in Visual Studio Code.
* Visual Studio 2022 can be installed later if required by the project.


# Appendix B — Useful PowerShell Commands

Compact commands to identify the Windows system, architecture, installed tools, and development environment.

## Windows version

```powershell
winver
```

Opens the Windows version dialog.

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber
```

Shows Windows edition, version, and build number.

## System architecture

```powershell
$env:PROCESSOR_ARCHITECTURE
```

Shows processor architecture, usually `AMD64`.

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object OSArchitecture
```

Shows whether Windows is 64-bit.

```powershell
Get-CimInstance Win32_Processor | Select-Object Name, Architecture
```

Shows CPU name and architecture code.

## Computer model

```powershell
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, TotalPhysicalMemory
```

Shows manufacturer, model, and RAM.

## RAM

```powershell
Get-CimInstance Win32_ComputerSystem | Select-Object @{Name="RAM_GB";Expression={[math]::Round($_.TotalPhysicalMemory / 1GB, 2)}}
```

Shows installed RAM in GB.

## Disk information

```powershell
Get-Volume
```

Shows drives, filesystem, size, and free space.

```powershell
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size
```

Shows whether the disk is SSD or HDD, if Windows can detect it.

## PowerShell administrator check

```powershell
([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
```

Returns `True` if PowerShell is running as Administrator.

## Execution policy

```powershell
Get-ExecutionPolicy -List
```

Shows script execution policy.

Temporary for current PowerShell only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Useful if a trusted local script is blocked.

## Installed program search

```powershell
winget list
```

Lists installed programs known to Windows Package Manager.

```powershell
winget list Visual
```

Searches installed programs containing `Visual`.

## Git

```powershell
git --version
```

Checks Git installation.

```powershell
git config --global user.name
git config --global user.email
```

Shows configured Git identity.

## VS Code

```powershell
code --version
```

Checks VS Code installation.

```powershell
code --list-extensions
```

Lists installed VS Code extensions.

```powershell
code --list-extensions --show-versions
```

Lists installed VS Code extensions with versions.

## .NET

```powershell
dotnet --version
```

Shows default .NET SDK version.

```powershell
dotnet --list-sdks
```

Lists installed .NET SDKs.

```powershell
dotnet --list-runtimes
```

Lists installed .NET runtimes.

## Node.js and npm

```powershell
node --version
npm --version
```

Checks Node.js and npm.

```powershell
npm list -g --depth=0
```

Lists globally installed npm packages.

## Angular CLI

```powershell
ng version
```

Shows Angular CLI and Angular environment.

If `ng` is not found:

```powershell
npm list -g @angular/cli
```

Checks whether Angular CLI is installed globally.

## Docker

```powershell
docker --version
docker compose version
```

Checks Docker and Docker Compose.

```powershell
docker info
```

Checks whether Docker Desktop / Docker Engine is running.

```powershell
docker ps
```

Lists running containers.

## Network

```powershell
ipconfig
```

Shows local network configuration.

```powershell
Test-NetConnection github.com -Port 443
```

Tests HTTPS connectivity to GitHub.

```powershell
Test-NetConnection dev.azure.com -Port 443
```

Tests HTTPS connectivity to Azure DevOps.

## Environment variables

```powershell
Get-ChildItem Env:
```

Lists environment variables.

```powershell
$env:PATH -split ';'
```

Shows PATH entries line by line.

## Current user and machine

```powershell
whoami
hostname
```

Shows current Windows user and computer name.

## Quick full diagnosis

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture
git --version
code --version
dotnet --list-sdks
node --version
npm --version
docker --version
```

Useful summary for support.


# Appendix C

### Waccess to Visual Studio 2022 when working from home?
 

1. **Installed on your company laptop**

   * You launch Visual Studio 2022 directly.
   * Works from office or home.

2. **Installed on a company server**

   * You connect using:

     * Remote Desktop (RDP)
     * VPN + Remote Desktop
     * Azure Virtual Desktop
     * Citrix
   * This is consistent with:

     > "Visual Studio 2022 läuft auf dem Server"
 

> "Visual Studio 2022 auf dem Server läuft. Wird dafür ein Remote-Zugang verwendet oder benötigen wir normalerweise nur VS Code?"

---
 

## Required

### 1. Visual Studio Code

Purpose:

* Main development environment
* Angular
* C#
* Git
* Markdown
* Codex

---

### 2. Angular Language Service (VS Code Extension)

Purpose:

* Angular IntelliSense
* Template validation
* Autocompletion

Required version:

```text
19.2.0
```

(if still required by the project)

---

### 3. C# Dev Kit

Purpose:

* C# development
* Debugging
* Project management

---

### 4. C#

Purpose:

* Language support for .NET projects

---

### 5. .NET Install Tool

Purpose:

* Automatically installs required .NET SDKs

---

### 6. Git

Purpose:

* Source code management
* Clone repositories
* Commit and push changes

Verify:

```powershell
git --version
```

---

### 7. GitLens

Purpose:

* Git history inside VS Code
* Author information
* File blame

---

### 8. Markdown All in One

Purpose:

* Documentation editing
* Table formatting
* TOC generation

---

### 9. markdownlint

Purpose:

* Markdown quality checks
* Consistent documentation

---

### 10. Codex

Purpose:

* AI coding assistant
* Code generation
* Refactoring
* Documentation help

Requires:

* ChatGPT/OpenAI account

---

### 11. ShareX

Purpose:

* Screenshots
* Documentation images
* Bug reports

---

### 12. OneNote

Purpose:

* Shared notes
* Meeting notes
* Project information

---

# Optional (ask first)

### Docker Desktop

Purpose:

* Containers
* Local development environments

Install only if requested.

---

### Dev Containers

Purpose:

* Open projects inside Docker containers

Install only if requested.

---

### Container Tools

Purpose:

* Manage containers from VS Code

Install only if requested.

---

### Visual Studio 2022

Purpose:

* Full Microsoft IDE
* Advanced .NET debugging

Probably not needed initially.

---

# First-Day Verification

After installation:

```powershell
git --version
code --version
dotnet --version
```

In VS Code check:

```text
Angular Language Service
C# Dev Kit
C#
.NET Install Tool
GitLens
Markdown All in One
markdownlint
Codex
```

If all of those are present, you are essentially ready for the first 2-hour onboarding session.
