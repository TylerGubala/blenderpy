# Welcome
Thank you for visiting the `blenderpy` repository, and viewing the contribution guidelines.

# Getting Started

Much of the Blender as a Python module build orchestration is provided by VS Code tasks. Some extensions are required to run some of the tasks. Please see the prerequisites.

## Prerequisites

1. [Visual Studio Code](https://code.visualstudio.com/)
    1. [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    2. [VS Code Tasks Shell Input](https://marketplace.visualstudio.com/items?itemName=augustocdias.tasks-shell-input)
2. [Docker](https://www.docker.com/)
3. [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) - (If on Windows) For faster Docker builds, otherwise Docker produces a warning
4. [Blender build requirements](https://wiki.blender.org/wiki/Building_Blender) - See your operating system's requirements here

To see how to build, head over to [the wiki](https://github.com/TylerGubala/blenderpy/wiki).

# Submit a bug report

If you find something that may be wrong with the code, please feel free to submit a bug report. Try and follow the guidelines outlined [here](https://github.com/TylerGubala/blenderpy/blob/master/.github/ISSUE_TEMPLATE/bug_report.md). I will get back with you.

# Submit a feature request

If you want some additional feature added to the repo, please try to follow the guidelines [here](https://github.com/TylerGubala/blenderpy/blob/master/.github/ISSUE_TEMPLATE/feature_request.md), similarly to the bug report, I am open to discussions, so don't hesitate to ask! Additionally, if you want to be a little more informal and discuss it prior, you can always join me in the [Discord](https://discord.gg/d5qqhzK)

# Create a Pull Request

Please when implimenting the pull request be sure to update the `setup.py` with any `install_requires` fields that may be necessary per your change. Describe in detail what the improvement is and we can talk about it.
