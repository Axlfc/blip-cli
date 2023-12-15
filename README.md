# blip-cli
CLI port of https://replicate.com/salesforce/blip

## Overview

This project automates the generation of BLIP captions for images using the Replicate platform.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Axlfc/blip-cli.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Script

If you have an image path as an argument:

#### GNU/Linux

<code>python3 img2txt.py "/path/to/your/image.jpg"</code>

#### Windows

<code>python img2txt.py "C:\Users\Your_Username\path\to\your\image.jpg"</code>

If you don't provide an argument, the script will prompt you to enter the image path.

### Image Captions Processing Functions

#### Bash
If you want that `blip_process_single_image` alias in GNU/Linux, you can edit `~/.bash_aliases` file and add:

> [!NOTE]  
> Make sure the line 'source ~/.bash_aliases' is present in ~/.bashrc if you encounter errors.

```bash
blip_process_single_image() {
    local script_path="path/to/img2txt.py"

    if [ -z "$1" ]; then
        echo "Usage: blip_process_single_image <image_path>"
        return 1
    fi

    local image_path="$1"
    python3 "$script_path" "$image_path"
}

blip_process_single_image "/path/to/single/image.jpg"
```

#### PowerShell
If you want to run a simple command `Invoke-BlipProcessSingleImage` to run BLIP Image Captioning in Windows Terminal, 
you can edit the 'C:\Users\Your_Username\Documents\WindowsPowershell\Microsoft.PowerShell_profile.ps1' file and add to it the following lines:

```powershell
function Invoke-BlipProcessSingleImage {
    param (
        [string]$ScriptPath = "C:\path\to\img2txt.py",
        [string]$ImagePath
    )

    if (-not $ImagePath) {
        Write-Host "Usage: Invoke-BlipProcessSingleImage -ImagePath <image_path>"
        return
    }

    & python $ScriptPath $ImagePath
}

Invoke-BlipProcessSingleImage -ImagePath "C:\path\to\single\image.jpg"
```

### Batch Image Processing

#### Bash

```bash
blip_process_batch_images() {
    local script_path="path/to/img2txt.py"

    if [ -z "$1" ]; then
        echo "Usage: blip_process_batch_images <image_folder>"
        return 1
    fi

    local folder_path="$1"
    for image in $folder_path/*; do
        python3 "$script_path" "$image"
    done
}

blip_process_batch_images "/path/to/image/folder"
```

#### PowerShell

```powershell
function Invoke-BlipProcessBatchImages {
    param (
        [string]$ScriptPath = "C:\path\to\img2txt.py",
        [string]$FolderPath
    )

    if (-not $FolderPath) {
        Write-Host "Usage: Invoke-BlipProcessBatchImages -FolderPath <image_folder>"
        return
    }

    Get-ChildItem $FolderPath | ForEach-Object {
        & python $ScriptPath $_.FullName
    }
}

Invoke-BlipProcessBatchImages -FolderPath "C:\path\to\image\folder"
```

> [!IMPORTANT]
> Adjust paths based on your project structure.