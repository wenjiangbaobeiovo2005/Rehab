# Kivy Installation Issue and Solutions

## Problem Description

During the GitHub Actions build process, you encountered the following error:

```
WARNING: Ignoring version 2.0.0 of kivy since it has invalid metadata:
Requested kivy==2.0.0 from https://files.pythonhosted.org/packages/bd/8f/9f7ba658034a58375380f77edc0c622e3c7de57c83cf7b6a09fe9f115b52/Kivy-2.0.0-cp39-cp39-manylinux2010_x86_64.whl (from -r requirements.txt (line 1)) has invalid metadata: Expected matching RIGHT_PARENTHESIS for LEFT_PARENTHESIS, after version specifier
    sys-platform (=="win32") ; extra == 'angle'
                 ~^
Please use pip<24.1 if you need to use this version.
```

This error occurs because Kivy version 2.0.0 has invalid metadata that is incompatible with pip versions 24.1 and above.

## Solutions

### Solution 1: Update to a newer Kivy version (Recommended)

We've updated the [requirements.txt](file:///c%3A/Users/23849/Desktop/%E6%B7%B1%E8%B9%B2/requirements.txt) file to use Kivy 2.3.0, which doesn't have the metadata issues:

```
kivy==2.3.0
opencv-python
mediapipe==0.8.9.1
numpy==1.21.2
requests==2.27.1
```

This is the recommended approach as it uses a more recent, stable version of Kivy.

### Solution 2: Use an older pip version

If you need to stick with Kivy 2.0.0 for compatibility reasons, you can use pip version < 24.1. We've provided an alternative requirements file [requirements_kivy2.0.0.txt](file:///c%3A/Users/23849/Desktop/%E6%B7%B1%E8%B9%B2/requirements_kivy2.0.0.txt) and updated the GitHub Actions workflows to use:

```bash
pip install "pip<24.1"
pip install -r requirements_kivy2.0.0.txt
```

## GitHub Actions Updates

We've updated both workflow files to ensure compatibility:
- [.github/workflows/android.yml](file:///c%3A/Users/23849/Desktop/%E6%B7%B1%E8%B9%B2/.github/workflows/android.yml)
- [.github/workflows/build-android.yml](file:///c%3A/Users/23849/Desktop/%E6%B7%B1%E8%B9%B2/.github/workflows/build-android.yml)

These workflows now explicitly use pip < 24.1 to avoid the metadata compatibility issue.

## Testing

A test script [test_kivy_install.py](file:///c%3A/Users/23849/Desktop/%E6%B7%B1%E8%B9%B2/test_kivy_install.py) has been created to verify that Kivy installation works correctly.

## Recommendation

We recommend using Solution 1 (Kivy 2.3.0) as it provides a more stable and up-to-date version of Kivy without requiring specific pip version constraints.