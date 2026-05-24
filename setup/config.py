SUPPORTED_OS = {
    "windows": {
        "git": ["winget install Git.Git"],
        "node": ["winget install OpenJS.NodeJS"],
        "python": ["winget install Python.Python.3"],
        "anaconda": ["winget install Anaconda.Anaconda3 --verbose"],
    },
    "darwin": {
        "git": ["brew install git"],
        "node": ["brew install node"],
        "python": ["brew install python"],
        "anaconda": ["brew install --cask anaconda"],
    },
    "linux": {
        "git": ["sudo apt install -y git"],
        "node": ["sudo apt install -y nodejs npm"],
        "python": ["sudo apt install -y python3"],
        "anaconda": ["wget https://anaconda.com"],
    },
}


VERIFY_INSTALLATION_COMMANDS = {
    "python": ["python3 --version", "python --version"],
    "js": ["node --version"],
    "ts": ["tsc --version"],
    "tsx": ["tsc --version"],
    "node": ["node --version"],
    "npm": ["npm --version"],
    "nb": ["jupyter notebook --version"],
    "lab": ["jupyter lab --version"],
    "anaconda": ["conda --version"],
    "react": ["npm list react", "npx react --version"],
    "nextjs": ["npx --no next --version", "next --version"],
    "git": ["git --version"],
}
