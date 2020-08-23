# Welcome
Thank you for visiting the `blenderpy` repository, and viewing the contribution guidelines.

By your visit here, the assumption is that you would like to contribute to the code base, or become a maintainer of a certain portion of the code. If not, and you were just looking to publish an issue, then you don't have to read all of this, and can simply go to the issues tracking page.

Your contributions are most welcome! This is a somewhat informal repository, in that there aren't many maintainers (just me as of writing 1<sup>st</sup> of May, 2019!) and I am always willing to help or provide some insight if you are doing some development with this.
## Quick Links
 - [Issue Tracker](https://github.com/TylerGubala/blenderpy/issues)
 - [Blender Artists Forum](https://blenderartists.org/t/pip-installable-bpy-module/1116741)
 - [Discord](https://discord.gg/d5qqhzK) (go to the `#blender-repos` channel)
# Get started
`blenderpy` is somewhat of a complicated solution. This repository actually doesn't do much on its own; it mostly exists so that we can control how the `bpy` required files get distributed (more [here](https://github.com/TylerGubala/blenderpy/issues/13)). For the building of the `bpy` files, the `bpy-build` repository is used (a requirement of this repository) and for the final placement of all the files, `bpy-ensure` is used (places the `/Scripts` file in the correct location, which has been an [issue](https://github.com/TylerGubala/blenderpy/issues/13) before).

Therefore in order to contribute to the project as a whole, you are going to want to check out two repos. Follow the steps below:
 1. Clone the repository `git clone https://github.com/TylerGubala/blenderpy` into the directory of your choice
 2. Clone the repository `git clone https://github.com/TylerGubala/bpy-build` into the directory of your choice
 3. `cd blenderpy`
 4. `mkdir venv`
 5. `cd venv`
 6. `py -3.6-32 -m venv 3.6-32` _optional_: replace 3.6-32 with your preferred python version
 7. `cd ..`
 8. `venv/3.6-32/Scripts/activate`
 9. `(3.6-32)py -m pip install -r requirements.txt`
10. `cd bpy-build`
11. `mkdir venv`
12. `cd venv`
13. `py -3.6-32 -m venv 3.6-32` _optional_: replace 3.6-32 with your preferred python version
14. `cd ..`
15. `venv/3.6-32/Scripts/activate`
16. `(3.6-32)py -m pip install -r requirements.txt`
17. `cd bpy-ensure`
18. `mkdir venv`
19. `cd venv`
20. `py -3.6-32 -m venv 3.6-32` _optional_: replace 3.6-32 with your preferred python version
21. `cd ..`
22. `venv/3.6-32/Scripts/activate`
23. `(3.6-32)py -m pip install -r requirements.txt`
24. _optional_: To watch the build process, run `bpy-build/setup.py` in your preferred coding environment with a debugger attached

# Submit a bug report

If you find something that may be wrong with the code, please feel free to submit a bug report. Try and follow the guidelines outlined [here](https://github.com/TylerGubala/blenderpy/blob/master/.github/ISSUE_TEMPLATE/bug_report.md). I will get back with you.

# Submit a feature request

If you want some additional feature added to the repo, please try to follow the guidelines [here](https://github.com/TylerGubala/blenderpy/blob/master/.github/ISSUE_TEMPLATE/feature_request.md), similarly to the bug report, I am open to discussions, so don't hesitate to ask! Additionally, if you want to be a little more informal and discuss it prior, you can always join me in the [Discord](https://discord.gg/d5qqhzK)

# Create a Pull Request

Please when implimenting the pull request be sure to update the `setup.py` with any `install_requires` fields that may be necessary per your change. Describe in detail what the improvement is and we can talk about it.
