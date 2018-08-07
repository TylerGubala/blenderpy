# blenderpy
Blender as a python module with easy-install

Meant for installation into a virtualenv or wherever, for unit testing of Blender extensions being authored, or developement of a Blender 3d-enabled Python application.

## Option 1 - Get prebuilt bdist_wheel from pypi

### Prerequisites

1. A supported python installation with pip installed

### Installation

`py -m pip install bpy`

## Option 2 - Build from sources using pypi

### Prerequisites

1. Windows users must have Visual Studio 2013 or later and C++ build tools installed to build from sources
2. Windows users must have an SVN provider to build from sources (see )
3. All users must `py -m pip install cmake` in their python environment to build from sources (currently adding it as a `setup_requires` does not install it properly); after build it may be uninstalled with `py -m pip uninstall cmake`
4. Users of Python versions below 3.6 must have `future-fstrings` installed `pip install -U future-fstrings`
5. Users of Python versions 3.4 and below will probably need to update `setuptools` `pip install -U setuptools`
6. Up-to-date `wheel`

### Installation

`py -m pip install bpy --no-binary`

### How it works

0. Create overriding classes CMakeExtension & BuildCMake, which inheirit from the setuptools classes; bpy is a python extension (.pyd) and an instance of CMakeExtension, BuildCMake is the command that is run when installing the extension from pip (or running setup.py)
1. Using GitPython, clone Blender sources from https://git.blender.org/
2. If on Windows, detect the installed version of Visual Studio and 64bit vs 32bit, and download the appropriate svn library based on that
3. Using cmake, configure blender as a python module per the Ideasman42 wiki page (now defunct) https://wiki.blender.org/wiki//User:Ideasman42/BlenderAsPyModule; configure this build solution in the build_temp directory of the bpy package
4. Using cmake, build the configured solution
5. Place the built binaries in the built extension parent directory (important!)
6. Relocate the /<Version> directory (i.e: /2.79) into the directory containing the executable from which this installation was spawned (where 'python.exe' is)
7. Clean up using the remaining functionality from the superclasses `build_ext` and `Extension`
8. bpy.pyd/ .so should now be installed into the site-packages

### Gotchas

I have not tested this for platforms other than Windows at the moment. More to come soon.

## Support this project

<a href="https://www.patreon.com/bePatron?u=3979551" data-patreon-widget-type="become-patron-button"><img src="https://cloakandmeeple.files.wordpress.com/2017/06/become_a_patron_button3x.png?w=610" width="150px"></a><script async src="https://c6.patreon.com/becomePatronButton.bundle.js"></script>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----MIIHNwYJKoZIhvcNAQcEoIIHKDCCByQCAQExggEwMIIBLAIBADCBlDCBjjELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAkNBMRYwFAYDVQQHEw1Nb3VudGFpbiBWaWV3MRQwEgYDVQQKEwtQYXlQYWwgSW5jLjETMBEGA1UECxQKbGl2ZV9jZXJ0czERMA8GA1UEAxQIbGl2ZV9hcGkxHDAaBgkqhkiG9w0BCQEWDXJlQHBheXBhbC5jb20CAQAwDQYJKoZIhvcNAQEBBQAEgYCG7kYuLzJn6JQyu58QIIOH9Poj3nL5wzLGSPxm3ecfYZdnFB8iIZxGzrG8jsiB8IMFYCFNstoCdgIRdv8ASK0lfA0Fplj4Qp8UzSvg0dKvOyuo07YljLj27pFqs84lKfzUJ1AZeFz1jXOFkaV6WzblmntsKQ4kOBHJEg0vrNC5rTELMAkGBSsOAwIaBQAwgbQGCSqGSIb3DQEHATAUBggqhkiG9w0DBwQImD0pWMUq0V2AgZBhGNUg1xyzrarelA9roAVra6I05WO4EKNPa2MdrmRvVC31LTeTS5Bit1yhvg1DK12GyQP7gD7kVCMEt4vzLxzgDsYgCUmFvl6cAGxpCNTG1DelKFYcQ37bCxGtSwjEeYfe/d+pBwBiEwlsuWNhK4BQThcvP/PKNlNvSW0Iej/lisiYjZYBV1ghYM4K8I1MlmKgggOHMIIDgzCCAuygAwIBAgIBADANBgkqhkiG9w0BAQUFADCBjjELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAkNBMRYwFAYDVQQHEw1Nb3VudGFpbiBWaWV3MRQwEgYDVQQKEwtQYXlQYWwgSW5jLjETMBEGA1UECxQKbGl2ZV9jZXJ0czERMA8GA1UEAxQIbGl2ZV9hcGkxHDAaBgkqhkiG9w0BCQEWDXJlQHBheXBhbC5jb20wHhcNMDQwMjEzMTAxMzE1WhcNMzUwMjEzMTAxMzE1WjCBjjELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAkNBMRYwFAYDVQQHEw1Nb3VudGFpbiBWaWV3MRQwEgYDVQQKEwtQYXlQYWwgSW5jLjETMBEGA1UECxQKbGl2ZV9jZXJ0czERMA8GA1UEAxQIbGl2ZV9hcGkxHDAaBgkqhkiG9w0BCQEWDXJlQHBheXBhbC5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMFHTt38RMxLXJyO2SmS+Ndl72T7oKJ4u4uw+6awntALWh03PewmIJuzbALScsTS4sZoS1fKciBGoh11gIfHzylvkdNe/hJl66/RGqrj5rFb08sAABNTzDTiqqNpJeBsYs/c2aiGozptX2RlnBktH+SUNpAajW724Nv2Wvhif6sFAgMBAAGjge4wgeswHQYDVR0OBBYEFJaffLvGbxe9WT9S1wob7BDWZJRrMIG7BgNVHSMEgbMwgbCAFJaffLvGbxe9WT9S1wob7BDWZJRroYGUpIGRMIGOMQswCQYDVQQGEwJVUzELMAkGA1UECBMCQ0ExFjAUBgNVBAcTDU1vdW50YWluIFZpZXcxFDASBgNVBAoTC1BheVBhbCBJbmMuMRMwEQYDVQQLFApsaXZlX2NlcnRzMREwDwYDVQQDFAhsaXZlX2FwaTEcMBoGCSqGSIb3DQEJARYNcmVAcGF5cGFsLmNvbYIBADAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4GBAIFfOlaagFrl71+jq6OKidbWFSE+Q4FqROvdgIONth+8kSK//Y/4ihuE4Ymvzn5ceE3S/iBSQQMjyvb+s2TWbQYDwcp129OPIbD9epdr4tJOUNiSojw7BHwYRiPh58S1xGlFgHFXwrEBb3dgNbMUa+u4qectsMAXpVHnD9wIyfmHMYIBmjCCAZYCAQEwgZQwgY4xCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJDQTEWMBQGA1UEBxMNTW91bnRhaW4gVmlldzEUMBIGA1UEChMLUGF5UGFsIEluYy4xEzARBgNVBAsUCmxpdmVfY2VydHMxETAPBgNVBAMUCGxpdmVfYXBpMRwwGgYJKoZIhvcNAQkBFg1yZUBwYXlwYWwuY29tAgEAMAkGBSsOAwIaBQCgXTAYBgkqhkiG9w0BCQMxCwYJKoZIhvcNAQcBMBwGCSqGSIb3DQEJBTEPFw0xODA4MDYyMjAxMjJaMCMGCSqGSIb3DQEJBDEWBBTpi8pDS59IpL1DXtj3V1goWjNNAzANBgkqhkiG9w0BAQEFAASBgITn4OUdSr1bgXGuyj/HaKvP9HHrJtiILcoGelesk4wuUooUVjG88colft5vfcY336L9SSz44FLkExBwbXHKxSaNuPIaneLwXWk8aUgbu6RmEp7TS0GNwkZ0ygCdoWIWSg/8VskhnSE7taX9y3r/0SIOtQ9m/Xhk9aYfPVJvNPcc-----END PKCS7-----
">
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
</form>