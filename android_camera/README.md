## Install Android SDK

Download and unzip sdkmanager into SDKROOT/tools
https://developer.android.com/studio/command-line/sdkmanager

```
$ cd $SDKROOT
$ tools/bin/sdkmanager --sdk_root=. "build-tools;28.0.3"
$ tools/bin/sdkmanager --sdk_root=. "platform-tools"
$ brew install gradle
```

## Prepare the build env

```
$ cd android_camera
$ echo "sdk.root=$SDKROOT" > local.properties
```

## Build the app
```
$ gradle build
```

## Run the app
```
$ gradle installDebug
```

