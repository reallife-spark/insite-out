---
title: neurosity-neurosity-class
source_url: https://docs.neurosity.co/docs/reference/classes/Neurosity
fetched_at: 2026-11-26T08:23:37+00:00
engine: defuddle
defuddle_version: 0.19.13
content_sha256: 033939e7046e680237f9141deb0b70b142d5642b1cea69a118b1802483593aac
status: captured
depth: 1
root_source: https://share.google/aimode/mhgoDgYotEKcIHMGo
---

---

## Class: Neurosity

Defined in: [Neurosity.ts:84](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L84)

Example

```typescript
import { Neurosity } from "@neurosity/sdk";

const neurosity = new Neurosity();
```

## Constructors

### Constructor

> **new Neurosity** (`options`): `Neurosity`

Defined in: [Neurosity.ts:127](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L127)

Creates new instance of the Neurosity SDK

```typescript
const neurosity = new Neurosity();
```

#### Parameters

##### options

[`SDKOptions`](https://docs.neurosity.co/docs/reference/interfaces/SDKOptions) = `{}`

#### Returns

`Neurosity`

## Accessors

### training

#### Get Signature

> **get** **training** (): `Training`

Defined in: [Neurosity.ts:1540](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1540)

Streaming modes:Wi-Fi

```typescript
neurosity.training.record({
  metric: "kinesis",
  label: "push"
});

neurosity.training.stop({
  metric: "kinesis",
  label: "push"
});
```

##### Returns

`Training`

Training methods

## Methods

### \_\_getApp()

> **\_\_getApp** (): `FirebaseApp`

Defined in: [Neurosity.ts:403](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L403)

**`Internal`**

Not user facing.

#### Returns

`FirebaseApp`

---

### accelerometer()

> **accelerometer** (): `Observable`< [`Accelerometer`](https://docs.neurosity.co/docs/reference/interfaces/Accelerometer) >

Defined in: [Neurosity.ts:837](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L837)

Streaming modes:Wi-FiBluetooth

Observes accelerometer data Supported by the Crown and Notion 2 devices.

```typescript
neurosity.accelerometer().subscribe(accelerometer => {
  console.log(accelerometer);
});

// { acceleration: ..., inclination: ..., orientation: ..., pitch: ..., roll: ..., x: ..., y: ..., z: ... }
```

#### Returns

`Observable`< [`Accelerometer`](https://docs.neurosity.co/docs/reference/interfaces/Accelerometer) >

Observable of accelerometer metric events

---

### addDevice()

> **addDevice** (`deviceId`): `Promise`\<`void`\>

Defined in: [Neurosity.ts:429](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L429)

Add a device to the user's account

```typescript
await neurosity.addDevice("[deviceId]");
```

#### Parameters

##### deviceId

`string`

#### Returns

`Promise`\<`void`\>

---

### addExperimentMarker()

> **addExperimentMarker** (`experimentId`, `marker`): `Promise`\<`string`\>

Defined in: [Neurosity.ts:1968](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1968)

Streaming modes:Wi-Fi

Adds a marker to an experiment recording and returns the marker's ID.

```typescript
await neurosity.addExperimentMarker(experimentId, {
  label: "drop",
  timestamp: Date.now()
});
```

#### Parameters

##### experimentId

`string`

The ID of the experiment

##### marker

[`ExperimentMarker`](https://docs.neurosity.co/docs/reference/type-aliases/ExperimentMarker)

The marker to add (`label` and `timestamp` required)

#### Returns

`Promise`\<`string`\>

The new marker's ID

---

### addMarker()

> **addMarker** (`label`): `Promise`\<`Action`\>

Defined in: [Neurosity.ts:708](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L708)

Streaming modes:Wi-FiBluetooth

Injects an EEG marker to data stream

```typescript
neurosity.addMarker("eyes-closed");

// later...

neurosity.addMarker("eyes-open");
```

#### Parameters

##### label

`string`

Name the label to inject

#### Returns

`Promise`\<`Action`\>

---

### brainwaves()

> **brainwaves** (`label`): `Observable`< [`Epoch`](https://docs.neurosity.co/docs/reference/interfaces/Epoch) | [`PSD`](https://docs.neurosity.co/docs/reference/interfaces/PSD) | [`PowerByBand`](https://docs.neurosity.co/docs/reference/interfaces/PowerByBand) >

Defined in: [Neurosity.ts:917](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L917)

Streaming modes:Wi-FiBluetooth

The `raw` brainwaves parameter emits epochs of 16 samples for Crown and 25 for Notion 1 and 2.

Example

```typescript
neurosity.brainwaves("raw").subscribe(brainwaves => {
  console.log(brainwaves);
});
```

Raw Unfiltered - The `rawUnfiltered` brainwaves parameter emits epochs of 16 samples for Crown and 25 for Notion 1 and 2.

Example

```typescript
neurosity.brainwaves("rawUnfiltered").subscribe(brainwaves => {
  console.log(brainwaves);
});
```

Power By Band - The `powerByBand` brainwaves parameter emits epochs 4 times a second. Every frequency label (e.g. beta) contains an average power value per channel.

Example

```typescript
neurosity.brainwaves("powerByBand").subscribe(brainwaves => {
  console.log(brainwaves);
});
```

Power Spectral Density (PSD) - The `psd` brainwaves parameter emits epochs 4 times a second. Every frequency label (e.g. alpha) contains the computed FFT (Fast Fourier transform) value per channel (see the `psd` property), as well as the frequency ranges (see the `freqs` property).

Example

```typescript
neurosity.brainwaves("psd").subscribe(brainwaves => {
  console.log(brainwaves);
});
```

#### Parameters

##### label

[`BrainwavesLabel`](https://docs.neurosity.co/docs/reference/type-aliases/BrainwavesLabel)

Name of metric properties to filter by

#### Returns

`Observable`< [`Epoch`](https://docs.neurosity.co/docs/reference/interfaces/Epoch) | [`PSD`](https://docs.neurosity.co/docs/reference/interfaces/PSD) | [`PowerByBand`](https://docs.neurosity.co/docs/reference/interfaces/PowerByBand) >

Observable of brainwaves metric events

---

### calm()

> **calm** (): `Observable`< [`Calm`](https://docs.neurosity.co/docs/reference/interfaces/Calm) >

Defined in: [Neurosity.ts:1201](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1201)

Streaming modes:Wi-FiBluetooth

Example

```typescript
neurosity.calm().subscribe(calm => {
  console.log(calm.probability);
});

// 0.45
// 0.47
// 0.53
// 0.51
// ...
```

#### Returns

`Observable`< [`Calm`](https://docs.neurosity.co/docs/reference/interfaces/Calm) >

Observable of calm events - awareness/calm alias

---

### changeSettings()

> **changeSettings** (`settings`): `Promise`\<`void`\>

Defined in: [Neurosity.ts:1505](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1505)

Streaming modes:Wi-Fi

Changes device settings programmatically. These settings can be also changed from the developer console under device settings.

Available settings \[\[Settings\]\]

Example

```typescript
neurosity.changeSettings({
  lsl: true
});
```

#### Parameters

##### settings

[`Settings`](https://docs.neurosity.co/docs/reference/interfaces/Settings)

#### Returns

`Promise`\<`void`\>

---

### createAccount()

> **createAccount** (`credentials`): `Promise`\<`any`\>

Defined in: [Neurosity.ts:1633](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1633)

Creates user account and automatically signs in with same credentials

#### Parameters

##### credentials

[`EmailAndPassword`](https://docs.neurosity.co/docs/reference/type-aliases/EmailAndPassword)

#### Returns

`Promise`\<`any`\>

user credential

---

### createApiKey()

> **createApiKey** (`data`): `Promise`\<`ApiKeyRecord`\>

Defined in: [Neurosity.ts:1684](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1684)

Creates API key to use to login with `{ apiKey }`.

#### Parameters

##### data

`CreateApiKeyRequest`

#### Returns

`Promise`\<`ApiKeyRecord`\>

API key record

---

### createBluetoothToken()

> **createBluetoothToken** (): `Promise`\<`string`\>

Defined in: [Neurosity.ts:1653](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1653)

**`Internal`**

Not user facing

Creates token (JWT) designed to authenticate and authorize Bluetooth clients/centrals.

#### Returns

`Promise`\<`string`\>

token

---

### createCustomToken()

> **createCustomToken** (): `Promise`< [`CustomToken`](https://docs.neurosity.co/docs/reference/type-aliases/CustomToken) >

Defined in: [Neurosity.ts:1665](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1665)

**`Internal`**

Not user facing yet

Creates custom token (JWT) to use to login with `{ customToken }`.

#### Returns

`Promise`< [`CustomToken`](https://docs.neurosity.co/docs/reference/type-aliases/CustomToken) >

custom token

---

### createOAuthURL()

> **createOAuthURL** (`config`): `Promise`\<`string`\>

Defined in: [Neurosity.ts:1777](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1777)

Create OAuth URL 💡 OAuth requires developers to register their apps with Neurosity [Read full OAuth guide](https://docs.neurosity.co/docs/api/oauth)

Creates client-specific OAuth URL. This is the first step of the OAuth workflow. Use this function to create a URL you can use to redirect users to the Neurosity sign-in page. 💡 This function is designed to only run on the server side for security reasons, as it requires your client secret.

```typescript
const { Neurosity } = require("@neurosity/sdk");

const neurosity = new Neurosity({
  autoSelectDevice: false
});

exports.handler = async function (event) {
  return neurosity
    .createOAuthURL({
      clientId: process.env.NEUROSITY_OAUTH_CLIENT_ID,
      clientSecret: process.env.NEUROSITY_OAUTH_CLIENT_SECRET,
      redirectUri: process.env.NEUROSITY_OAUTH_CLIENT_REDIRECT_URI,
      responseType: "token",
      state: Math.random().toString().split(".")[1],
      scope: [
        "read:devices-info",
        "read:devices-status",
        "read:signal-quality",
        "read:brainwaves"
      ]
    })
    .then((url) => ({
      statusCode: 200,
      body: JSON.stringify({ url })
    }))
    .catch((error) => ({
      statusCode: 400,
      body: JSON.stringify(error.response.data)
    }));
};
```

#### Parameters

##### config

[`OAuthConfig`](https://docs.neurosity.co/docs/reference/type-aliases/OAuthConfig)

#### Returns

`Promise`\<`string`\>

custom token

---

### createUserExperiment()

> **createUserExperiment** (`options`): `Promise`\<`string`\>

Defined in: [Neurosity.ts:1922](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1922)

Streaming modes:Wi-Fi

Creates a new experiment owned by the authenticated user and returns its generated ID. Pair with [Neurosity.onUserExperiments](#onuserexperiments) to observe it, and [Neurosity.updateUserExperiment](#updateuserexperiment) to fill in details as the user works.

```typescript
const experimentId = await neurosity.createUserExperiment({
  deviceId: device.deviceId,
  name: "Left hand pinch",
  labels: ["leftHandPinch"]
});
```

#### Parameters

##### options

[`CreateExperimentOptions`](https://docs.neurosity.co/docs/reference/type-aliases/CreateExperimentOptions)

Experiment options (`deviceId` required; `name`/`labels` optional)

#### Returns

`Promise`\<`string`\>

The new experiment's ID

---

### deleteAccount()

> **deleteAccount** (): `Promise`\<`void`\>

Defined in: [Neurosity.ts:1641](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1641)

Removes all devices from an account and then deletes the account

#### Returns

`Promise`\<`void`\>

---

### deleteUserExperiment()

> **deleteUserExperiment** (`experimentId`): `Promise`\<`void`\>

Defined in: [Neurosity.ts:1899](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1899)

Streaming modes:Wi-Fi

Deletes a specific experiment provided an experiment ID

```typescript
await neurosity.deleteUserExperiment(experiment.id);
```

#### Parameters

##### experimentId

`string`

The ID of the Experiment

#### Returns

`Promise`\<`void`\>

void

---

### disconnect()

> **disconnect** (): `Promise`\<`void`\>

Defined in: [Neurosity.ts:660](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L660)

Streaming modes:Wi-FiBluetooth

Ends database connection

```typescript
await neurosity.disconnect();
```

#### Returns

`Promise`\<`void`\>

---

### focus()

> **focus** (): `Observable`< [`Focus`](https://docs.neurosity.co/docs/reference/interfaces/Focus) >

Defined in: [Neurosity.ts:1382](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1382)

Streaming modes:Wi-FiBluetooth

Example

```typescript
neurosity.focus().subscribe(focus => {
  console.log(focus.probability);
});

// 0.56
// 0.46
// 0.31
// 0.39
// ...
```

#### Returns

`Observable`< [`Focus`](https://docs.neurosity.co/docs/reference/interfaces/Focus) >

Observable of focus events - awareness/focus alias

---

### getDevices()

> **getDevices** (): `Promise`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) \[\]>

Defined in: [Neurosity.ts:534](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L534)

Get user devices

Returns a list of devices claimed by the user authenticated.

```typescript
const devices = await neurosity.getDevices();
console.log(devices);
```

#### Returns

`Promise`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) \[\]>

---

### getHapticEffects()

> **getHapticEffects** (): [`HapticEffects`](https://docs.neurosity.co/docs/reference/type-aliases/HapticEffects)

Defined in: [Neurosity.ts:817](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L817)

```typescript
const effects = neurosity.getHapticEffects();
```

#### Returns

[`HapticEffects`](https://docs.neurosity.co/docs/reference/type-aliases/HapticEffects)

---

### getInfo()

> **getInfo** (): `Promise`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) >

Defined in: [Neurosity.ts:607](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L607)

```typescript
const info = await neurosity.getInfo();
```

#### Returns

`Promise`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) >

---

### getOAuthToken()

> **getOAuthToken** (`query`): `Promise`< [`OAuthQueryResult`](https://docs.neurosity.co/docs/reference/type-aliases/OAuthQueryResult) >

Defined in: [Neurosity.ts:1828](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1828)

Get OAuth Token 💡 OAuth requires developers to register their apps with Neurosity [Read full OAuth guide](https://docs.neurosity.co/docs/api/oauth)

Gets client-specific OAuth token for a given userId.

💡 This function is designed to only run on the server side for security reasons, as it requires your client secret. Here's an example of a cloud function that receives a `userId` via query params and loads the client id and client secret securely via environment variables.

```typescript
const { Neurosity } = require("@neurosity/sdk");

const neurosity = new Neurosity({
  autoSelectDevice: false
});

exports.handler = async function (event) {
  const userId = event.queryStringParameters?.userId;

  return neurosity
    .getOAuthToken({
      clientId: process.env.NEUROSITY_OAUTH_CLIENT_ID,
      clientSecret: process.env.NEUROSITY_OAUTH_CLIENT_SECRET,
      userId
    })
    .then((token) => ({
      statusCode: 200,
      body: JSON.stringify(token)
    }))
    .catch((error) => ({
      statusCode: 200,
      body: JSON.stringify(error.response.data)
    }));
};
```

#### Parameters

##### query

[`OAuthQuery`](https://docs.neurosity.co/docs/reference/type-aliases/OAuthQuery)

#### Returns

`Promise`< [`OAuthQueryResult`](https://docs.neurosity.co/docs/reference/type-aliases/OAuthQueryResult) >

custom token

---

### getSelectedDevice()

> **getSelectedDevice** (): `Promise`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) >

Defined in: [Neurosity.ts:588](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L588)

Get selected device

```typescript
const selectedDevice = await neurosity.getSelectedDevice();
console.log(selectedDevice);
```

#### Returns

`Promise`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) >

---

### getTimesyncOffset()

> **getTimesyncOffset** (): `number`

Defined in: [Neurosity.ts:1727](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1727)

**`Internal`**

Not user facing yet

Gets the offset between the device's clock and the client's clock Requires option.timesync to be true

#### Returns

`number`

timesyncOffset

---

### goOffline()

> **goOffline** (): `void`

Defined in: [Neurosity.ts:1614](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1614)

**`Internal`**

Proof of Concept for disconnecting db

#### Returns

`void`

---

### goOnline()

> **goOnline** (): `void`

Defined in: [Neurosity.ts:1622](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1622)

**`Internal`**

Proof of Concept for resuming db connection

#### Returns

`void`

---

### haptics()

> **haptics** (`effects`): `Promise`\<`any`\>

Defined in: [Neurosity.ts:768](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L768)

Streaming modes:Wi-FiBluetooth

Queue haptic motor commands

To queue haptic P7 only,

```typescript
await neurosity.haptics({
  P7: ["tripleClick100"]
});
```

To queue both motors at the same time

```typescript
await neurosity.haptics({
  P7: [neurosity.getHapticEffects().strongClick100],
  P8: [neurosity.getHapticEffects().strongClick100]
});
```

You can queue different commands to the motors too

```typescript
const effects = neurosity.getHapticEffects();
await neurosity.haptics({
  P7: [effects.transitionRampUpLongSmooth1_0_to_100,
        effects.transitionRampDownLongSmooth1_100_to_0],
  P8: [effects.strongClick100]
});
```

#### Parameters

##### effects

`any`

Effects to queue. The key of the object passed should be the location of the motor to queue. Each key can be an array of up to 7 commands. There is no haptic support for model version 1, Notion DK1. The Haptic motor's location is positioned in reference to the 10-10 EEG system used to label the channels of the Crown's EEG sensors. Notion 2 and Crown have haptics at P7 and P8. A list of haptic commands can be found on./utils/hapticCodes.ts - there are about 127 of them!

#### Returns

`Promise`\<`any`\>

---

### kinesis()

> **kinesis** (`label`): `Observable`< [`Kinesis`](https://docs.neurosity.co/docs/reference/interfaces/Kinesis) >

Defined in: [Neurosity.ts:1410](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1410)

Streaming modes:Wi-Fi

#### Parameters

##### label

`string`

Name of metric properties to filter by

#### Returns

`Observable`< [`Kinesis`](https://docs.neurosity.co/docs/reference/interfaces/Kinesis) >

Observable of kinesis metric events

---

### login()

> **login** (`credentials`): `Promise`\<`void`\>

Defined in: [Neurosity.ts:382](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L382)

Starts user session

```typescript
await neurosity.login({
  email: "...",
  password: "..."
});
```

#### Parameters

##### credentials

[`Credentials`](https://docs.neurosity.co/docs/reference/type-aliases/Credentials)

#### Returns

`Promise`\<`void`\>

---

### logout()

> **logout** (): `Promise`\<`void`\>

Defined in: [Neurosity.ts:395](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L395)

Ends user session

```typescript
await neurosity.logout();
// session has ended
```

#### Returns

`Promise`\<`void`\>

---

### onAuthStateChanged()

> **onAuthStateChanged** (): `Observable`\<`any`\>

Defined in: [Neurosity.ts:418](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L418)

Subscribe to auth state changes

Streams the state of the auth session. If user has logged in, the user object will be set. When logged out, the user object will be null.

```typescript
neurosity.onAuthStateChanged().subscribe((user) => {
  console.log(user);
});
```

#### Returns

`Observable`\<`any`\>

---

### onDeviceChange()

> **onDeviceChange** (): `Observable`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) >

Defined in: [Neurosity.ts:637](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L637)

Observes selected device

```typescript
neurosity.onDeviceChange().subscribe(device => {
 console.log(device);
});
```

#### Returns

`Observable`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) >

---

### onExperimentMarkers()

> **onExperimentMarkers** (`experimentId`): `Observable`< [`ExperimentMarker`](https://docs.neurosity.co/docs/reference/type-aliases/ExperimentMarker) \[\]>

Defined in: [Neurosity.ts:2040](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L2040)

Streaming modes:Wi-Fi

Observes the markers dropped during an experiment recording, sorted by timestamp. Each marker includes its `id`.

```typescript
neurosity.onExperimentMarkers(experimentId).subscribe((markers) => {
  console.log(markers);
});
```

#### Parameters

##### experimentId

`string`

The ID of the experiment

#### Returns

`Observable`< [`ExperimentMarker`](https://docs.neurosity.co/docs/reference/type-aliases/ExperimentMarker) \[\]>

Observable of the experiment's markers

---

### onUserClaimsChange()

> **onUserClaimsChange** (): `Observable`\<`UserClaims`\>

Defined in: [Neurosity.ts:520](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L520)

Subscribe to user claims changes

```typescript
neurosity.onUserClaimsChange().subscribe((userClaims) => {
  console.log(userClaims);
});
```

#### Returns

`Observable`\<`UserClaims`\>

---

### onUserDevicesChange()

> **onUserDevicesChange** (): `Observable`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) \[\]>

Defined in: [Neurosity.ts:497](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L497)

Subscribe to user devices changes

```typescript
neurosity.onUserDevicesChange().subscribe((devices) => {
  console.log(devices);
});
```

#### Returns

`Observable`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) \[\]>

---

### onUserExperiments()

> **onUserExperiments** (): `Observable`< [`Experiment`](https://docs.neurosity.co/docs/reference/type-aliases/Experiment) \[\]>

Defined in: [Neurosity.ts:1883](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1883)

Streaming modes:Wi-Fi

Observes and returns a list of all Kinesis `experiments` and all subsequent experiment changes. Here's an example of how to get a list of all Kinesis labels that have been trained:

```typescript
const getUniqueLabels = (experiments) => {
  const labels = experiments.flatMap((experiment) => experiment.labels);
  // only return unique labels
  return [...new Set(labels)];
}

neurosity.onUserExperiments().subscribe((experiments) => {
  console.log(experiments);
  console.log("labels", getUniqueLabels(experiments));
});

// [{ id: '...', deviceId: '...', labels: [ 'drop' ], name: 'Lightgray cheetah', timestamp: 1577908381552, totalTrials: 16, userId: '...' }]
// ["drop", "lift", "push"]
```

#### Returns

`Observable`< [`Experiment`](https://docs.neurosity.co/docs/reference/type-aliases/Experiment) \[\]>

Observable of `experiments` events

---

### osVersion()

> **osVersion** (): `Observable`\<`string`\>

Defined in: [Neurosity.ts:1350](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1350)

Streaming modes:Wi-Fi

Observes the current OS version and all subsequent version changes in real-time.

```typescript
neurosity.osVersion().subscribe((osVersion) => {
  console.log(osVersion);
});

// "16.0.0"
```

#### Returns

`Observable`\<`string`\>

Observable of `osVersion` events. e.g 16.0.0

---

### predictions()

> **predictions** (`label`): `Observable`\<`any`\>

Defined in: [Neurosity.ts:1436](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1436)

Streaming modes:Wi-Fi

#### Parameters

##### label

`string`

Name of metric properties to filter by

#### Returns

`Observable`\<`any`\>

Observable of predictions metric events

---

### record()

> **record** (`options`): `Promise`< [`RecordingResult`](https://docs.neurosity.co/docs/reference/interfaces/RecordingResult) >

Defined in: [Neurosity.ts:974](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L974)

Streaming modes:Wi-Fi

Records raw brainwave data for a specified duration and saves it as a dataset. The recording is stored in cloud storage and a metadata record is created in Firestore. If the network is unavailable, the recording is saved locally on the device and uploaded automatically when connectivity is restored.

```typescript
const result = await neurosity.record({
  label: "eyes-closed",
  duration: 60000
});

console.log(result.id); // Firestore record ID
```

With all options:

```typescript
const result = await neurosity.record({
  name: "Morning session",
  label: "focus-training",
  duration: 120000,
  experimentId: "exp-001"
});
```

#### Parameters

##### options

[`RecordingOptions`](https://docs.neurosity.co/docs/reference/interfaces/RecordingOptions)

Recording options including label and duration

#### Returns

`Promise`< [`RecordingResult`](https://docs.neurosity.co/docs/reference/interfaces/RecordingResult) >

Promise resolving to the recording result

---

### removeApiKey()

> **removeApiKey** (`apiKeyId`): `Promise`\<`RemoveApiKeyResponse`\>

Defined in: [Neurosity.ts:1704](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1704)

Removes API key

#### Parameters

##### apiKeyId

`string`

#### Returns

`Promise`\<`RemoveApiKeyResponse`\>

void

---

### removeDevice()

> **removeDevice** (`deviceId`): `Promise`\<`void`\>

Defined in: [Neurosity.ts:450](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L450)

Remove a device from the user's account

```typescript
await neurosity.removeDevice("[deviceId]");
```

#### Parameters

##### deviceId

`string`

#### Returns

`Promise`\<`void`\>

---

### removeOAuthAccess()

> **removeOAuthAccess** (): `Promise`< [`OAuthRemoveResponse`](https://docs.neurosity.co/docs/reference/type-aliases/OAuthRemoveResponse) >

Defined in: [Neurosity.ts:1854](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1854)

Remove OAuth Access 💡 OAuth requires developers to register their apps with Neurosity [Read full OAuth guide](https://docs.neurosity.co/docs/api/oauth)

Removes client-specific OAuth token for a given userId. Requires SDK to be signed in with OAuth custom token.

```typescript
await neurosity.removeOAuthAccess().catch((error) => {
  // handle error here...
});
```

#### Returns

`Promise`< [`OAuthRemoveResponse`](https://docs.neurosity.co/docs/reference/type-aliases/OAuthRemoveResponse) >

custom token

---

### saveExperimentPrediction()

> **saveExperimentPrediction** (`experimentId`, `prediction`): `Promise`\<`string`\>

Defined in: [Neurosity.ts:2018](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L2018)

Streaming modes:Wi-Fi

Saves a model prediction for an experiment and returns the prediction's ID. `timestamp` defaults to a server timestamp when omitted.

```typescript
await neurosity.saveExperimentPrediction(experimentId, {
  trial: 0,
  label: "leftHandPinch",
  probability: 0.92,
  metric: "kinesis"
});
```

#### Parameters

##### experimentId

`string`

The ID of the experiment

##### prediction

[`ExperimentPrediction`](https://docs.neurosity.co/docs/reference/type-aliases/ExperimentPrediction)

The prediction payload

#### Returns

`Promise`\<`string`\>

The new prediction's ID

---

### saveExperimentTrial()

> **saveExperimentTrial** (`experimentId`, `trial`): `Promise`\<`string`\>

Defined in: [Neurosity.ts:1992](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1992)

Streaming modes:Wi-Fi

Saves a training trial result for an experiment and returns the trial's ID. `timestamp` defaults to a server timestamp when omitted.

```typescript
await neurosity.saveExperimentTrial(experimentId, {
  label: "leftHandPinch",
  baseline: false
});
```

#### Parameters

##### experimentId

`string`

The ID of the experiment

##### trial

[`ExperimentTrial`](https://docs.neurosity.co/docs/reference/type-aliases/ExperimentTrial)

The trial payload

#### Returns

`Promise`\<`string`\>

The new trial's ID

---

### selectDevice()

> **selectDevice** (`deviceSelector`): `Promise`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) >

Defined in: [Neurosity.ts:563](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L563)

Select Device

Rarely necessary, but useful when the user owns multiple devices.

A common use case for manually selecting a device is when you wish to build a device dropdown a user can select from, instead of collecting the Device Id from the user ahead of time.

The 3 steps to manually selecting a device are:

- Set `autoSelectDevice` to false when instantiating the `Neurosity` class.
- Authenticate with your Neurosity account to access your devices by calling the `neurosity.login(...)` function.
- Call the `neurosity.selectDevice(...)` function with a device selector function.
```typescript
const devices = await neurosity.selectDevice((devices) =>
  devices.find((device) => device.deviceNickname === "Crown-A1B")
);

console.log(devices);
```

> If you own multiple devices, and don't pass `autoSelectDevice`, then the first device on the list will be automatically selected.

For more info, check out the "Device Selection" guide.

#### Parameters

##### deviceSelector

(`devices`) => [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo)

#### Returns

`Promise`< [`DeviceInfo`](https://docs.neurosity.co/docs/reference/interfaces/DeviceInfo) >

---

### setEmulatorStatus()

> **setEmulatorStatus** (`deviceId`, `patch`): `Promise`\<`void`\>

Defined in: [Neurosity.ts:2062](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L2062)

Streaming modes:Wi-Fi

Sets simulated status fields on an **emulator** device (e.g. toggling `state` or `charging`). Intended for emulator/dev tooling — on real hardware the device owns its status.

```typescript
await neurosity.setEmulatorStatus(deviceId, { state: "online" });
await neurosity.setEmulatorStatus(deviceId, { charging: true });
```

#### Parameters

##### deviceId

`string`

The emulator device's ID

##### patch

[`EmulatorStatusPatch`](https://docs.neurosity.co/docs/reference/type-aliases/EmulatorStatusPatch)

Status fields to set (`state` and/or `charging`)

#### Returns

`Promise`\<`void`\>

void

---

### settings()

> **settings** (): `Observable`< [`Settings`](https://docs.neurosity.co/docs/reference/interfaces/Settings) >

Defined in: [Neurosity.ts:1321](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1321)

Streaming modes:Wi-Fi

Observes last state of `settings` and all subsequent `settings` changes

```typescript
neurosity.settings().subscribe(settings => {
  console.log(settings.lsl);
});

// true
// ...
```

#### Returns

`Observable`< [`Settings`](https://docs.neurosity.co/docs/reference/interfaces/Settings) >

Observable of `settings` metric events

---

### signalQuality()

> **signalQuality** (): `Observable`< [`SignalQuality`](https://docs.neurosity.co/docs/reference/interfaces/SignalQuality) >

Defined in: [Neurosity.ts:1240](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1240)

Streaming modes:Wi-FiBluetooth

Observes signal quality data where each property is the name of the channel and the value includes the standard deviation and a status set by the device

```typescript
neurosity.signalQuality().subscribe(signalQuality => {
  console.log(signalQuality);
});

// { FC6: { standardDeviation: 3.5, status: "good" }, C3: {...}, ... }
```

#### Returns

`Observable`< [`SignalQuality`](https://docs.neurosity.co/docs/reference/interfaces/SignalQuality) >

Observable of signalQuality metric events

---

### signalQualityV2()

> **signalQualityV2** (): `Observable`< [`SignalQualityV2`](https://docs.neurosity.co/docs/reference/interfaces/SignalQualityV2) >

Defined in: [Neurosity.ts:1281](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1281)

Streaming modes:Wi-FiBluetooth

Observes signal quality with normalized scores (0-1) per channel and an overall score.

```typescript
neurosity.signalQualityV2().subscribe(quality => {
  console.log(quality.overall.score);  // 0-1
  console.log(quality.byChannel.CP3.score);  // 0-1
});

// { timestamp: 1234567890, overall: { score: 0.85 }, byChannel: { CP3: { score: 0.9 }, ... } }
```

#### Returns

`Observable`< [`SignalQualityV2`](https://docs.neurosity.co/docs/reference/interfaces/SignalQualityV2) >

Observable of signalQualityV2 metric events

---

### startRecording()

> **startRecording** (`options`): `Promise`< [`RecordingHandle`](https://docs.neurosity.co/docs/reference/interfaces/RecordingHandle) >

Defined in: [Neurosity.ts:1056](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1056)

Streaming modes:Wi-Fi

Starts a variable-length brainwave recording and returns a handle for controlling it. Use this when you need UI control over the recording lifecycle (progress, cancel, stop-and-save).

```typescript
const recording = await neurosity.startRecording({
  label: "eyes-closed",
  maxDuration: 120000 // 2 minute max
});

// Track progress
recording.elapsed$.subscribe(ms => {
  console.log(`Recording: ${(ms / 1000).toFixed(0)}s`);
});

// Stop and save after some time
const result = await recording.stop();
console.log(result.id);

// Or cancel without saving
await recording.cancel();
```

#### Parameters

##### options

[`StartRecordingOptions`](https://docs.neurosity.co/docs/reference/interfaces/StartRecordingOptions)

Recording options including label and maxDuration

#### Returns

`Promise`< [`RecordingHandle`](https://docs.neurosity.co/docs/reference/interfaces/RecordingHandle) >

Promise resolving to a RecordingHandle

---

### status()

> **status** (): `Observable`< [`DeviceStatus`](https://docs.neurosity.co/docs/reference/interfaces/DeviceStatus) >

Defined in: [Neurosity.ts:1472](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1472)

Streaming modes:Wi-FiBluetooth

Observes last state of `status` and all subsequent `status` changes

```typescript
neurosity.status().subscribe(status => {
  console.log(status.state);
});

// "online"
// ...
```

#### Returns

`Observable`< [`DeviceStatus`](https://docs.neurosity.co/docs/reference/interfaces/DeviceStatus) >

Observable of `status` metric events

---

### streamingState()

> **streamingState** (): `Observable`<{ `activeMode`: `STREAMING_TYPE`; `connected`: `boolean`; `streamingMode`: [`STREAMING_MODE`](https://docs.neurosity.co/docs/reference/enumerations/STREAMING_MODE); }>

Defined in: [Neurosity.ts:211](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L211)

Subscribe to the device's streaming state changes and the current strategy

Streams the current mode of streaming (wifi or bluetooth).

```typescript
neurosity.streamingState().subscribe((streamingState) => {
  console.log(streamingState);
  // { streamingMode: "wifi-only", activeMode: "wifi", connected: true }
});
```

#### Returns

`Observable`<{ `activeMode`: `STREAMING_TYPE`; `connected`: `boolean`; `streamingMode`: [`STREAMING_MODE`](https://docs.neurosity.co/docs/reference/enumerations/STREAMING_MODE); }>

---

### transferDevice()

> **transferDevice** (`options`): `Promise`\<`void`\>

Defined in: [Neurosity.ts:474](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L474)

Transfer a device to the user's account

```typescript
await neurosity.transferDevice({
  deviceId: "[deviceId]",
  newOwnerEmail: "[newOwnerEmail]"
});
```

#### Parameters

##### options

`TransferDeviceOptions`

#### Returns

`Promise`\<`void`\>

---

### updateUserExperiment()

> **updateUserExperiment** (`experimentId`, `patch`): `Promise`\<`void`\>

Defined in: [Neurosity.ts:1945](https://github.com/neurosity/neurosity-sdk-js/blob/fe0fe332bf6cb9d3954cc12b2358becbcd264f06/src/Neurosity.ts#L1945)

Streaming modes:Wi-Fi

Updates fields on an existing experiment (e.g. name, notes, labels, totalTrials).

```typescript
await neurosity.updateUserExperiment(experimentId, {
  name: "Renamed experiment",
  labels: ["leftHandPinch", "rightHandPinch"]
});
```

#### Parameters

##### experimentId

`string`

The ID of the experiment

##### patch

`Partial`\<`Omit`< [`Experiment`](https://docs.neurosity.co/docs/reference/type-aliases/Experiment), `"id"` | `"userId"`\>>

Partial experiment fields to merge (`id`/`userId` cannot be changed)

#### Returns

`Promise`\<`void`\>

void
