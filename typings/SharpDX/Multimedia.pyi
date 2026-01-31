from __future__ import annotations
from enum import IntEnum, IntFlag
from typing import Any, ClassVar, Generic, TypeVar, overload
import SharpDX

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")

class AudclntSharemode(IntEnum):
    Shared = 0
    Exclusive = 1

class AudioEndpointRole(IntEnum):
    Console = 0
    Multimedia = 1
    Communications = 2

class AudioSessionState(IntEnum):
    AudioSessionStateInactive = 0
    AudioSessionStateActive = 1
    AudioSessionStateExpired = 2

class AudioStreamCategory(IntEnum):
    Other = 0
    ForegroundOnlyMedia = 1
    Communications = 3
    Alerts = 4
    SoundEffects = 5
    GameEffects = 6
    GameMedia = 7
    GameChat = 8
    Speech = 9
    Movie = 10
    Media = 11

class FourCC:
    Empty: ClassVar[FourCC]
    @overload
    def __init__(self, fourCC: str) -> None: ...
    @overload
    def __init__(self, byte1: Any, byte2: Any, byte3: Any, byte4: Any) -> None: ...
    @overload
    def __init__(self, fourCC: int) -> None: ...
    @overload
    def __init__(self, fourCC: int) -> None: ...
    @overload
    def Equals(self, other: FourCC) -> bool: ...
    @overload
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @overload
    def ToString(self) -> str: ...
    @overload
    def ToString(self, format: str, formatProvider: Any) -> str: ...

class RiffChunk:
    Stream: Any
    Type: FourCC
    Size: int
    DataPosition: int
    IsList: bool
    IsHeader: bool
    def __init__(self, stream: Any, type: FourCC, size: int, dataPosition: int, isList: bool = ..., isHeader: bool = ...) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetData(self) -> list[int]: ...
    def GetDataAs(self) -> T: ...
    def GetDataAsArray(self) -> list[T]: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...

class RiffParser:
    ChunkStack: Any
    Current: RiffChunk
    def __init__(self, input: Any) -> None: ...
    def Ascend(self) -> None: ...
    def Descend(self) -> None: ...
    def Dispose(self) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetAllChunks(self) -> Any: ...
    def GetEnumerator(self) -> Any: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    def MoveNext(self) -> bool: ...
    def Reset(self) -> None: ...
    def ToString(self) -> str: ...

class SoundStream:
    DecodedPacketsInfo: list[int]
    Format: WaveFormat
    CanRead: bool
    CanSeek: bool
    CanWrite: bool
    Position: int
    Length: int
    CanTimeout: bool
    ReadTimeout: int
    WriteTimeout: int
    def __init__(self, stream: Any) -> None: ...
    def BeginRead(self, buffer: list[int], offset: int, count: int, callback: Any, state: Any) -> Any: ...
    def BeginWrite(self, buffer: list[int], offset: int, count: int, callback: Any, state: Any) -> Any: ...
    def Close(self) -> None: ...
    @overload
    def CopyTo(self, destination: Any) -> None: ...
    @overload
    def CopyTo(self, destination: Any, bufferSize: int) -> None: ...
    @overload
    def CopyToAsync(self, destination: Any) -> Any: ...
    @overload
    def CopyToAsync(self, destination: Any, bufferSize: int) -> Any: ...
    @overload
    def CopyToAsync(self, destination: Any, cancellationToken: Any) -> Any: ...
    @overload
    def CopyToAsync(self, destination: Any, bufferSize: int, cancellationToken: Any) -> Any: ...
    def Dispose(self) -> None: ...
    def DisposeAsync(self) -> Any: ...
    def EndRead(self, asyncResult: Any) -> int: ...
    def EndWrite(self, asyncResult: Any) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def Flush(self) -> None: ...
    @overload
    def FlushAsync(self) -> Any: ...
    @overload
    def FlushAsync(self, cancellationToken: Any) -> Any: ...
    def GetHashCode(self) -> int: ...
    def GetLifetimeService(self) -> Any: ...
    def GetType(self) -> Any: ...
    def InitializeLifetimeService(self) -> Any: ...
    @overload
    def Read(self, buffer: list[int], offset: int, count: int) -> int: ...
    @overload
    def Read(self, buffer: Any) -> int: ...
    @overload
    def ReadAsync(self, buffer: list[int], offset: int, count: int) -> Any: ...
    @overload
    def ReadAsync(self, buffer: list[int], offset: int, count: int, cancellationToken: Any) -> Any: ...
    @overload
    def ReadAsync(self, buffer: Any, cancellationToken: Any = ...) -> Any: ...
    def ReadAtLeast(self, buffer: Any, minimumBytes: int, throwOnEndOfStream: bool = ...) -> int: ...
    def ReadAtLeastAsync(self, buffer: Any, minimumBytes: int, throwOnEndOfStream: bool = ..., cancellationToken: Any = ...) -> Any: ...
    def ReadByte(self) -> int: ...
    @overload
    def ReadExactly(self, buffer: Any) -> None: ...
    @overload
    def ReadExactly(self, buffer: list[int], offset: int, count: int) -> None: ...
    @overload
    def ReadExactlyAsync(self, buffer: Any, cancellationToken: Any = ...) -> Any: ...
    @overload
    def ReadExactlyAsync(self, buffer: list[int], offset: int, count: int, cancellationToken: Any = ...) -> Any: ...
    def Seek(self, offset: int, origin: Any) -> int: ...
    def SetLength(self, value: int) -> None: ...
    def ToDataStream(self) -> SharpDX.DataStream: ...
    def ToString(self) -> str: ...
    @overload
    def Write(self, buffer: list[int], offset: int, count: int) -> None: ...
    @overload
    def Write(self, buffer: Any) -> None: ...
    @overload
    def WriteAsync(self, buffer: list[int], offset: int, count: int) -> Any: ...
    @overload
    def WriteAsync(self, buffer: list[int], offset: int, count: int, cancellationToken: Any) -> Any: ...
    @overload
    def WriteAsync(self, buffer: Any, cancellationToken: Any = ...) -> Any: ...
    def WriteByte(self, value: int) -> None: ...

class Speakers(IntFlag):
    None_ = 0
    FrontLeft = 1
    FrontRight = 2
    FrontCenter = 4
    LowFrequency = 8
    BackLeft = 16
    BackRight = 32
    FrontLeftOfCenter = 64
    FrontRightOfCenter = 128
    BackCenter = 256
    SideLeft = 512
    SideRight = 1024
    TopCenter = 2048
    TopFrontLeft = 4096
    TopFrontCenter = 8192
    TopFrontRight = 16384
    TopBackLeft = 32768
    TopBackCenter = 65536
    TopBackRight = 131072
    Reserved = 2147221504
    All = -2147483648

class SpeakersExtensions:
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @staticmethod
    def ToChannelCount(speakers: Speakers) -> int: ...
    def ToString(self) -> str: ...

class UsageId(IntEnum):
    KeyboardNoevent = 0
    GenericPointer = 1
    SportBaseballBat = 1
    Consumerctrl = 1
    DigitizerDigitizer = 1
    LedNumLock = 1
    VrBelt = 1
    HapticsSimpleController = 1
    AlphanumericAlphanumericDisplay = 1
    SimulationFlightSimulationDevice = 1
    TelephonyPhone = 1
    KeyboardRollover = 1
    Game3dGameController = 1
    GenericMouse = 2
    VrBodySuit = 2
    SportGolfClub = 2
    DigitizerPen = 2
    LedCapsLock = 2
    AlphanumericBitmappedDisplay = 2
    SimulationAutomobileSimulationDevice = 2
    GamePinballDevice = 2
    KeyboardPostfail = 2
    TelephonyAnsweringMachine = 2
    SimulationTankSimulationDevice = 3
    DigitizerLightPen = 3
    KeyboardUndefined = 3
    SportRowingMachine = 3
    VrFlexor = 3
    GameGunDevice = 3
    TelephonyMessageControls = 3
    LedScrollLock = 3
    KeyboardAA = 4
    SportTreadmill = 4
    LedCompose = 4
    VrGlove = 4
    TelephonyHandset = 4
    GenericJoystick = 4
    SimulationSpaceshipSimulationDevice = 4
    DigitizerTouchScreen = 4
    SimulationSubmarineSimulationDevice = 5
    VrHeadTracker = 5
    GenericGamepad = 5
    TelephonyHeadset = 5
    DigitizerTouchPad = 5
    LedKana = 5
    SimulationSailingSimulationDevice = 6
    DigitizerWhiteBoard = 6
    LedPower = 6
    GenericKeyboard = 6
    VrHeadMountedDisplay = 6
    TelephonyKeypad = 6
    GenericKeypad = 7
    SimulationMotorcycleSimulationDevice = 7
    DigitizerCoordMeasuring = 7
    LedShift = 7
    VrHandTracker = 7
    TelephonyProgrammableButton = 7
    SimulationSportsSimulationDevice = 8
    GenericMultiAxisController = 8
    LedDoNotDisturb = 8
    VrOculometer = 8
    Digitizer3dDigitizer = 8
    VrVest = 9
    LedMute = 9
    SimulationAirplaneSimulationDevice = 9
    GenericTabletPcSystemCtl = 9
    DigitizerStereoPlotter = 9
    DigitizerArticulatedArm = 10
    VrAnimatronicDevice = 10
    SimulationHelicopterSimulationDevice = 10
    LedToneEnable = 10
    LedHighCutFilter = 11
    DigitizerArmature = 11
    SimulationMagicCarpetSimulationDevice = 11
    SimulationBicycleSimulationDevice = 12
    LedLowCutFilter = 12
    DigitizerMultiPoint = 12
    LedEqualizerEnable = 13
    DigitizerFreeSpaceWand = 13
    GenericPortableDeviceControl = 13
    GenericInteractiveControl = 14
    LedSoundFieldOn = 14
    LedSurroundFieldOn = 15
    HapticsWaveformList = 16
    LedRepeat = 16
    LedStereo = 17
    HapticsDurationList = 17
    LedSamplingRateDetect = 18
    LedSpinning = 19
    LedCav = 20
    LedClv = 21
    LedRecordingFormatDet = 22
    LedOffHook = 23
    LedRing = 24
    LedMessageWaiting = 25
    LedDataMode = 26
    LedBatteryOperation = 27
    LedBatteryOk = 28
    LedBatteryLow = 29
    KeyboardZZ = 29
    LedSpeaker = 30
    KeyboardOne = 30
    LedHeadSet = 31
    AlphanumericDisplayAttributesReport = 32
    GenericDeviceBatteryStrength = 32
    DigitizerStylus = 32
    GamePointOfView = 32
    VrStereoEnable = 32
    LedHold = 32
    CameraAutoFocus = 32
    HapticsAutoTrigger = 32
    SimulationFlightControlStick = 32
    DigitizerPuck = 33
    VrDisplayEnable = 33
    MsBthHfDialnumber = 33
    LedMicrophone = 33
    GameTurnRightLeft = 33
    GenericDeviceWirelessChannel = 33
    HapticsManualTrigger = 33
    CameraShutter = 33
    SimulationFlightStick = 33
    AlphanumericAsciiCharacterSet = 33
    GamePitchForwardBack = 34
    DigitizerFinger = 34
    GenericDeviceWirelessId = 34
    LedCoverage = 34
    HapticsAutoAssociatedControl = 34
    MsBthHfDialmemory = 34
    SimulationCyclicControl = 34
    AlphanumericDataReadBack = 34
    HapticsIntensity = 35
    GameRollRightLeft = 35
    AlphanumericFontReadBack = 35
    LedNightMode = 35
    SimulationCyclicTrim = 35
    GenericDeviceDiscoverWirelessControl = 35
    AlphanumericDisplayControlReport = 36
    LedSendCalls = 36
    GenericDeviceSecurityCodeCharEntered = 36
    HapticsRepeatCount = 36
    TelephonyRedial = 36
    SimulationFlightYoke = 36
    GameMoveRightLeft = 36
    GenericDeviceSecurityCodeCharErased = 37
    TelephonyTransfer = 37
    AlphanumericClearDisplay = 37
    GameMoveForwardBack = 37
    HapticsRetriggerPeriod = 37
    SimulationTrackControl = 37
    LedCallPickup = 37
    GenericDeviceSecurityCodeCleared = 38
    TelephonyDrop = 38
    LedConference = 38
    AlphanumericDisplayEnable = 38
    GameMoveUpDown = 38
    HapticsWaveformVendorPage = 38
    AlphanumericScreenSaverDelay = 39
    KeyboardZero = 39
    HapticsWaveformVendorId = 39
    GameLeanRightLeft = 39
    LedStandBy = 39
    GameLeanForwardBack = 40
    HapticsWaveformCutoffTime = 40
    LedCameraOn = 40
    KeyboardReturn = 40
    AlphanumericScreenSaverEnable = 40
    KeyboardEscape = 41
    AlphanumericVerticalScroll = 41
    GamePovHeight = 41
    LedCameraOff = 41
    TelephonyLine = 42
    KeyboardDelete = 42
    AlphanumericHorizontalScroll = 42
    LedOnLine = 42
    GameFlipper = 42
    AlphanumericCharacterReport = 43
    GameSecondaryFlipper = 43
    LedOffLine = 43
    AlphanumericDisplayData = 44
    GameBump = 44
    LedBusy = 44
    LedReady = 45
    GameNewGame = 45
    TelephonyRingEnable = 45
    AlphanumericDisplayStatus = 45
    GameShootBall = 46
    AlphanumericStatusNotReady = 46
    LedPaperOut = 46
    AlphanumericStatusReady = 47
    GamePlayer = 47
    LedPaperJam = 47
    DigitizerTipPressure = 48
    GenericX = 48
    GameGunBolt = 48
    AlphanumericErrNotALoadableCharacter = 48
    SportOar = 48
    LedRemote = 48
    GenericY = 49
    LedForward = 49
    TelephonySend = 49
    AlphanumericErrFontDataCannotBeRead = 49
    SportSlope = 49
    GameGunClip = 49
    DigitizerBarrelPressure = 49
    SportRate = 50
    LedReverse = 50
    AlphanumericCursorPositionReport = 50
    DigitizerInRange = 50
    GameGunSelector = 50
    GenericZ = 50
    GenericRx = 51
    AlphanumericRow = 51
    DigitizerTouch = 51
    LedStop = 51
    SportStickSpeed = 51
    GameGunSingleShot = 51
    GameGunBurst = 52
    SportStickFaceAngle = 52
    GenericRy = 52
    DigitizerUntouch = 52
    LedRewind = 52
    AlphanumericColumn = 52
    DigitizerTap = 53
    AlphanumericRows = 53
    GameGunAutomatic = 53
    LedFastForward = 53
    GenericRz = 53
    SportHeelToe = 53
    GameGunSafety = 54
    LedPlay = 54
    AlphanumericColumns = 54
    DigitizerQuality = 54
    SportFollowThrough = 54
    GenericSlider = 54
    DigitizerDataValid = 55
    AlphanumericCursorPixelPositioning = 55
    GameGamepadFireJump = 55
    SportTempo = 55
    GenericDial = 55
    LedPause = 55
    GenericWheel = 56
    LedRecord = 56
    AlphanumericCursorMode = 56
    SportStickType = 56
    DigitizerTransducerIndex = 56
    KeyboardCapsLock = 57
    GenericHatswitch = 57
    DigitizerTabletFuncKeys = 57
    SportHeight = 57
    LedError = 57
    AlphanumericCursorEnable = 57
    GameGamepadTrigger = 57
    GenericCountedBuffer = 58
    DigitizerProgChangeKeys = 58
    AlphanumericCursorBlink = 58
    LedSelectedIndicator = 58
    KeyboardF1 = 58
    AlphanumericFontReport = 59
    LedInUseIndicator = 59
    KeyboardF2 = 59
    GenericByteCount = 59
    DigitizerBatteryStrength = 59
    LedMultiModeIndicator = 60
    GenericMotionWakeup = 60
    KeyboardF3 = 60
    AlphanumericFontData = 60
    DigitizerInvert = 60
    KeyboardF4 = 61
    AlphanumericCharWidth = 61
    LedIndicatorOn = 61
    DigitizerXTilt = 61
    GenericStart = 61
    KeyboardF5 = 62
    DigitizerYTilt = 62
    AlphanumericCharHeight = 62
    LedIndicatorFlash = 62
    GenericSelect = 62
    DigitizerAzimuth = 63
    LedIndicatorSlowBlink = 63
    AlphanumericCharSpacingHorizontal = 63
    KeyboardF6 = 63
    DigitizerAltitude = 64
    GenericVx = 64
    AlphanumericCharSpacingVertical = 64
    KeyboardF7 = 64
    LedIndicatorFastBlink = 64
    LedIndicatorOff = 65
    KeyboardF8 = 65
    AlphanumericUnicodeCharSet = 65
    GenericVy = 65
    DigitizerTwist = 65
    KeyboardF9 = 66
    AlphanumericFont7Segment = 66
    GenericVz = 66
    LedFlashOnTime = 66
    DigitizerTipSwitch = 66
    LedSlowBlinkOnTime = 67
    GenericVbrx = 67
    KeyboardF10 = 67
    Alphanumeric7SegmentDirectMap = 67
    DigitizerSecondaryTipSwitch = 67
    KeyboardF11 = 68
    DigitizerBarrelSwitch = 68
    LedSlowBlinkOffTime = 68
    AlphanumericFont14Segment = 68
    GenericVbry = 68
    KeyboardF12 = 69
    LedFastBlinkOnTime = 69
    DigitizerEraser = 69
    GenericVbrz = 69
    Alphanumeric14SegmentDirectMap = 69
    LedFastBlinkOffTime = 70
    KeyboardPrintScreen = 70
    AlphanumericDisplayBrightness = 70
    GenericVno = 70
    DigitizerTabletPick = 70
    LedIndicatorColor = 71
    AlphanumericDisplayContrast = 71
    GenericFeatureNotification = 71
    KeyboardScrollLock = 71
    AlphanumericCharacterAttribute = 72
    LedRed = 72
    GenericResolutionMultiplier = 72
    AlphanumericAttributeReadback = 73
    LedGreen = 73
    LedAmber = 74
    AlphanumericAttributeData = 74
    LedGenericIndicator = 75
    AlphanumericCharAttrEnhance = 75
    AlphanumericCharAttrUnderline = 76
    KeyboardDeleteForward = 76
    LedSystemSuspend = 76
    AlphanumericCharAttrBlink = 77
    LedExternalPower = 77
    SportPutter = 80
    Sport1Iron = 81
    Sport2Iron = 82
    KeyboardNumLock = 83
    Sport3Iron = 83
    Sport4Iron = 84
    Sport5Iron = 85
    Sport6Iron = 86
    Sport7Iron = 87
    Sport8Iron = 88
    Sport9Iron = 89
    Sport10Iron = 90
    Sport11Iron = 91
    SportSandWedge = 92
    SportLoftWedge = 93
    SportPowerWedge = 94
    Sport1Wood = 95
    Sport3Wood = 96
    Sport5Wood = 97
    Sport7Wood = 98
    Sport9Wood = 99
    KeyboardF13 = 104
    KeyboardF14 = 105
    KeyboardF15 = 106
    KeyboardF16 = 107
    KeyboardF17 = 108
    KeyboardF18 = 109
    KeyboardF19 = 110
    KeyboardF20 = 111
    KeyboardF21 = 112
    KeyboardF22 = 113
    KeyboardF23 = 114
    KeyboardF24 = 115
    GenericSystemCtl = 128
    AlphanumericBitmapSizeX = 128
    AlphanumericBitmapSizeY = 129
    GenericSysctlPower = 129
    GenericSysctlSleep = 130
    AlphanumericBitDepthFormat = 131
    GenericSysctlWake = 131
    AlphanumericDisplayOrientation = 132
    GenericSysctlContextMenu = 132
    AlphanumericPaletteReport = 133
    GenericSysctlMainMenu = 133
    AlphanumericPaletteDataSize = 134
    GenericSysctlAppMenu = 134
    AlphanumericPaletteDataOffset = 135
    GenericSysctlHelpMenu = 135
    AlphanumericPaletteData = 136
    GenericSysctlMenuExit = 136
    GenericSysctlMenuSelect = 137
    GenericSysctlMenuRight = 138
    AlphanumericBlitReport = 138
    GenericSysctlMenuLeft = 139
    AlphanumericBlitRectangleX1 = 139
    GenericSysctlMenuUp = 140
    AlphanumericBlitRectangleY1 = 140
    AlphanumericBlitRectangleX2 = 141
    GenericSysctlMenuDown = 141
    AlphanumericBlitRectangleY2 = 142
    GenericSysctlColdRestart = 142
    AlphanumericBlitData = 143
    GenericSysctlWarmRestart = 143
    GenericDpadUp = 144
    AlphanumericSoftButton = 144
    GenericDpadDown = 145
    AlphanumericSoftButtonId = 145
    AlphanumericSoftButtonSide = 146
    GenericDpadRight = 146
    AlphanumericSoftButtonOffset1 = 147
    GenericDpadLeft = 147
    AlphanumericSoftButtonOffset2 = 148
    AlphanumericSoftButtonReport = 149
    ConsumerChannelIncrement = 156
    ConsumerChannelDecrement = 157
    GenericSysctlDock = 160
    GenericSysctlUndock = 161
    GenericSysctlSetup = 162
    GenericSysctlSysBreak = 163
    GenericSysctlSysDbgBreak = 164
    GenericSysctlAppBreak = 165
    GenericSysctlAppDbgBreak = 166
    GenericSysctlMute = 167
    GenericSysctlHibernate = 168
    TelephonyKeypad0 = 176
    ConsumerPlay = 176
    SimulationAileron = 176
    GenericSysctlDispInvert = 176
    SimulationAileronTrim = 177
    GenericSysctlDispInternal = 177
    ConsumerPause = 177
    GenericSysctlDispExternal = 178
    SimulationAntiTorqueControl = 178
    ConsumerRecord = 178
    GenericSysctlDispBoth = 179
    ConsumerFastForward = 179
    SimulationAutopiolotEnable = 179
    SimulationChaffRelease = 180
    GenericSysctlDispDual = 180
    ConsumerRewind = 180
    ConsumerScanNextTrack = 181
    SimulationCollectiveControl = 181
    GenericSysctlDispToggle = 181
    SimulationDiveBrake = 182
    GenericSysctlDispSwap = 182
    ConsumerScanPrevTrack = 182
    ConsumerStop = 183
    SimulationElectronicCountermeasures = 183
    GenericSysctlDispAutoscale = 183
    SimulationElevator = 184
    SimulationElevatorTrim = 185
    SimulationRudder = 186
    SimulationThrottle = 187
    SimulationFlightCommunications = 188
    SimulationFlareRelease = 189
    SimulationLandingGear = 190
    SimulationToeBrake = 191
    TelephonyKeypadD = 191
    SimulationTrigger = 192
    SimulationWeaponsArm = 193
    SimulationWeaponsSelect = 194
    SimulationWingFlaps = 195
    SimulationAccellerator = 196
    SimulationBrake = 197
    SimulationClutch = 198
    SimulationShifter = 199
    SimulationSteering = 200
    GenericSystemDisplayRotationLockButton = 201
    SimulationTurretDirection = 201
    SimulationBarrelElevation = 202
    GenericSystemDisplayRotationLockSliderSwitch = 202
    SimulationDivePlane = 203
    GenericControlEnable = 203
    SimulationBallast = 204
    SimulationBicycleCrank = 205
    ConsumerPlayPause = 205
    SimulationHandleBars = 206
    SimulationFrontBrake = 207
    ConsumerGamedvrOpenGamebar = 208
    SimulationRearBrake = 208
    ConsumerGamedvrToggleRecord = 209
    ConsumerGamedvrRecordClip = 210
    ConsumerGamedvrScreenshot = 211
    ConsumerGamedvrToggleIndicator = 212
    ConsumerGamedvrToggleMicrophone = 213
    ConsumerGamedvrToggleCamera = 214
    ConsumerGamedvrToggleBroadcast = 215
    KeyboardLctrl = 224
    ConsumerVolume = 224
    ConsumerBalance = 225
    KeyboardLshft = 225
    KeyboardLalt = 226
    ConsumerMute = 226
    KeyboardLgui = 227
    ConsumerBass = 227
    ConsumerTreble = 228
    KeyboardRctrl = 228
    KeyboardRshft = 229
    ConsumerBassBoost = 229
    ConsumerSurroundMode = 230
    KeyboardRalt = 230
    ConsumerLoudness = 231
    KeyboardRgui = 231
    ConsumerMpx = 232
    ConsumerVolumeIncrement = 233
    ConsumerVolumeDecrement = 234
    TelephonyHostAvailable = 241
    ConsumerBassIncrement = 338
    ConsumerBassDecrement = 339
    ConsumerTrebleIncrement = 340
    ConsumerTrebleDecrement = 341
    ConsumerAlConfiguration = 387
    ConsumerAlEmail = 394
    ConsumerAlCalculator = 402
    ConsumerAlBrowser = 404
    ConsumerAlSearch = 454
    ConsumerAcSearch = 545
    ConsumerAcGoto = 546
    ConsumerAcHome = 547
    ConsumerAcBack = 548
    ConsumerAcForward = 549
    ConsumerAcStop = 550
    ConsumerAcRefresh = 551
    ConsumerAcPrevious = 552
    ConsumerAcNext = 553
    ConsumerAcBookmarks = 554
    ConsumerAcPan = 568
    ConsumerExtendedKeyboardAttributesCollection = 704
    ConsumerKeyboardFormFactor = 705
    ConsumerKeyboardKeyType = 706
    ConsumerKeyboardPhysicalLayout = 707
    ConsumerVendorSpecificKeyboardPhysicalLayout = 708
    ConsumerKeyboardIetfLanguageTagIndex = 709
    ConsumerImplementedKeyboardInputAssistControls = 710
    HapticsWaveformBegin = 4096
    HapticsWaveformStop = 4097
    HapticsWaveformNull = 4098
    HapticsWaveformClick = 4099
    HapticsWaveformBuzz = 4100
    HapticsWaveformRumble = 4101
    HapticsWaveformPress = 4102
    HapticsWaveformRelease = 4103
    HapticsWaveformEnd = 8191
    HapticsWaveformVendorBegin = 8192
    HapticsWaveformVendorEnd = 12287

class UsagePage(IntEnum):
    Undefined = 0
    Generic = 1
    Simulation = 2
    Vr = 3
    Sport = 4
    Game = 5
    GenericDevice = 6
    Keyboard = 7
    Led = 8
    Button = 9
    Ordinal = 10
    Telephony = 11
    Consumer = 12
    Digitizer = 13
    Haptics = 14
    Pid = 15
    Unicode = 16
    Alphanumeric = 20
    Sensor = 32
    Medical = 64
    MonitorPage0 = 128
    MonitorPage1 = 129
    MonitorPage2 = 130
    MonitorPage3 = 131
    PowerPage0 = 132
    PowerPage1 = 133
    PowerPage2 = 134
    PowerPage3 = 135
    Barcode = 140
    BarcodeScanner = 140
    WeighingDevice = 141
    Scale = 141
    MagneticStripeReader = 142
    Msr = 142
    CameraControl = 144
    Arcade = 145
    VendorDefinedBegin = -256
    MicrosoftBluetoothHandsfree = -13
    VendorDefinedEnd = -1

class WaveFormat:
    Encoding: WaveFormatEncoding
    Channels: int
    SampleRate: int
    AverageBytesPerSecond: int
    BlockAlign: int
    BitsPerSample: int
    ExtraSize: int
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, sampleRate: int, channels: int) -> None: ...
    @overload
    def __init__(self, rate: int, bits: int, channels: int) -> None: ...
    @overload
    def __init__(self, br: Any) -> None: ...
    def ConvertLatencyToByteSize(self, milliseconds: int) -> int: ...
    @staticmethod
    def CreateALawFormat(sampleRate: int, channels: int) -> WaveFormat: ...
    @staticmethod
    def CreateCustomFormat(tag: WaveFormatEncoding, sampleRate: int, channels: int, averageBytesPerSecond: int, blockAlign: int, bitsPerSample: int) -> WaveFormat: ...
    @staticmethod
    def CreateIeeeFloatWaveFormat(sampleRate: int, channels: int) -> WaveFormat: ...
    @staticmethod
    def CreateMuLawFormat(sampleRate: int, channels: int) -> WaveFormat: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @overload
    @staticmethod
    def MarshalFrom(rawdata: list[int]) -> WaveFormat: ...
    @overload
    @staticmethod
    def MarshalFrom(pointer: Any) -> WaveFormat: ...
    @staticmethod
    def MarshalToPtr(format: WaveFormat) -> Any: ...
    def ToString(self) -> str: ...

class WaveFormatAdpcm:
    SamplesPerBlock: int
    Coefficients1: list[int]
    Coefficients2: list[int]
    Encoding: WaveFormatEncoding
    Channels: int
    SampleRate: int
    AverageBytesPerSecond: int
    BlockAlign: int
    BitsPerSample: int
    ExtraSize: int
    def __init__(self, rate: int, channels: int, blockAlign: int = ...) -> None: ...
    def ConvertLatencyToByteSize(self, milliseconds: int) -> int: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...

class WaveFormatEncoding(IntEnum):
    Unknown = 0
    Pcm = 1
    Adpcm = 2
    IeeeFloat = 3
    Vselp = 4
    IbmCvsd = 5
    Alaw = 6
    Mulaw = 7
    Dts = 8
    Drm = 9
    Wmavoice9 = 10
    Wmavoice10 = 11
    OkiAdpcm = 16
    DviAdpcm = 17
    ImaAdpcm = 17
    MediaspaceAdpcm = 18
    SierraAdpcm = 19
    G723Adpcm = 20
    Digistd = 21
    Digifix = 22
    DialogicOkiAdpcm = 23
    MediavisionAdpcm = 24
    CuCodec = 25
    HpDynVoice = 26
    YamahaAdpcm = 32
    Sonarc = 33
    DspgroupTruespeech = 34
    Echosc1 = 35
    AudiofileAf36 = 36
    Aptx = 37
    AudiofileAf10 = 38
    Prosody1612 = 39
    Lrc = 40
    DolbyAc2 = 48
    DefaultGsm610 = 49
    Msnaudio = 50
    AntexAdpcme = 51
    ControlResVqlpc = 52
    Digireal = 53
    Digiadpcm = 54
    ControlResCr10 = 55
    NmsVbxadpcm = 56
    CsImaadpcm = 57
    Echosc3 = 58
    RockwellAdpcm = 59
    RockwellDigitalk = 60
    Xebec = 61
    G721Adpcm = 64
    G728Celp = 65
    Msg723 = 66
    IntelG7231 = 67
    IntelG729 = 68
    SharpG726 = 69
    Mpeg = 80
    Rt24 = 82
    Pac = 83
    Mpeglayer3 = 85
    LucentG723 = 89
    Cirrus = 96
    Espcm = 97
    Voxware = 98
    CanopusAtrac = 99
    G726Adpcm = 100
    G722Adpcm = 101
    Dsat = 102
    DsatDisplay = 103
    VoxwareByteAligned = 105
    VoxwareAc8 = 112
    VoxwareAc10 = 113
    VoxwareAc16 = 114
    VoxwareAc20 = 115
    VoxwareRt24 = 116
    VoxwareRt29 = 117
    VoxwareRt29hw = 118
    VoxwareVr12 = 119
    VoxwareVr18 = 120
    VoxwareTq40 = 121
    VoxwareSc3 = 122
    VoxwareSc31 = 123
    Softsound = 128
    VoxwareTq60 = 129
    Msrt24 = 130
    G729A = 131
    MviMvi2 = 132
    DfG726 = 133
    DfGsm610 = 134
    Isiaudio = 136
    Onlive = 137
    MultitudeFtSx20 = 138
    InfocomItsG721Adpcm = 139
    ConvediaG729 = 140
    Congruency = 141
    Sbc24 = 145
    DolbyAc3Spdif = 146
    MediasonicG723 = 147
    Prosody8kbps = 148
    ZyxelAdpcm = 151
    PhilipsLpcbb = 152
    Packed = 153
    MaldenPhonytalk = 160
    RacalRecorderGsm = 161
    RacalRecorderG720A = 162
    RacalRecorderG7231 = 163
    RacalRecorderTetraAcelp = 164
    NecAac = 176
    RawAac1 = 255
    RhetorexAdpcm = 256
    Irat = 257
    VivoG723 = 273
    VivoSiren = 274
    PhilipsCelp = 288
    PhilipsGrundig = 289
    DigitalG723 = 291
    SanyoLdAdpcm = 293
    SiprolabAceplnet = 304
    SiprolabAcelp4800 = 305
    SiprolabAcelp8v3 = 306
    SiprolabG729 = 307
    SiprolabG729A = 308
    SiprolabKelvin = 309
    VoiceageAmr = 310
    G726ADPCM = 320
    DictaphoneCelp68 = 321
    DictaphoneCelp54 = 322
    QualcommPurevoice = 336
    QualcommHalfrate = 337
    Tubgsm = 341
    Msaudio1 = 352
    Wmaudio2 = 353
    Wmaudio3 = 354
    WmaudioLossless = 355
    Wmaspdif = 356
    UnisysNapAdpcm = 368
    UnisysNapUlaw = 369
    UnisysNapAlaw = 370
    UnisysNap16k = 371
    SycomAcmSyc008 = 372
    SycomAcmSyc701G726L = 373
    SycomAcmSyc701Celp54 = 374
    SycomAcmSyc701Celp68 = 375
    KnowledgeAdventureAdpcm = 376
    FraunhoferIisMpeg2Aac = 384
    DtsDs = 400
    CreativeAdpcm = 512
    CreativeFastspeech8 = 514
    CreativeFastspeech10 = 515
    UherAdpcm = 528
    UleadDvAudio = 533
    UleadDvAudio1 = 534
    Quarterdeck = 544
    IlinkVc = 560
    RawSport = 576
    EsstAc3 = 577
    GenericPassthru = 585
    IpiHsx = 592
    IpiRpelp = 593
    Cs2 = 608
    SonyScx = 624
    SonyScy = 625
    SonyAtrac3 = 626
    SonySpc = 627
    TelumAudio = 640
    TelumIaAudio = 641
    NorcomVoiceSystemsAdpcm = 645
    FmTownsSnd = 768
    Micronas = 848
    MicronasCelp833 = 849
    BtvDigital = 1024
    IntelMusicCoder = 1025
    IndeoAudio = 1026
    QdesignMusic = 1104
    On2Vp7Audio = 1280
    On2Vp6Audio = 1281
    VmeVmpcm = 1664
    Tpc = 1665
    LightwaveLossless = 2222
    Oligsm = 4096
    Oliadpcm = 4097
    Olicelp = 4098
    Olisbc = 4099
    Oliopr = 4100
    LhCodec = 4352
    LhCodecCelp = 4353
    LhCodecSbc8 = 4354
    LhCodecSbc12 = 4355
    LhCodecSbc16 = 4356
    Norris = 5120
    Isiaudio2 = 5121
    SoundspaceMusicompress = 5376
    MpegAdtsAac = 5632
    MpegRawAac = 5633
    MpegLoas = 5634
    NokiaMpegAdtsAac = 5640
    NokiaMpegRawAac = 5641
    VodafoneMpegAdtsAac = 5642
    VodafoneMpegRawAac = 5643
    MpegHeaac = 5648
    VoxwareRt24Speech = 6172
    SonicfoundryLossless = 6513
    InningsTelecomAdpcm = 6521
    LucentSx8300p = 7175
    LucentSx5363s = 7180
    Cuseeme = 7939
    NtcsoftAlf2cmAcm = 8132
    Dvm = 8192
    Dts2 = 8193
    Makeavis = 13075
    DivioMpeg4Aac = 16707
    NokiaAdaptiveMultirate = 16897
    DivioG726 = 16963
    LeadSpeech = 17228
    LeadVorbis = 22092
    WavpackAudio = 22358
    OggVorbisMode1 = 26447
    OggVorbisMode2 = 26448
    OggVorbisMode3 = 26449
    OggVorbisMode1Plus = 26479
    OggVorbisMode2Plus = 26480
    OggVorbisMode3Plus = 26481
    Alac = 27745
    Tag3COMNbx = 28672
    Opus = 28751
    FaadAac = 28781
    AmrNb = 29537
    AmrWb = 29538
    AmrWp = 29539
    GsmAmrCbr = 31265
    GsmAmrVbrSid = 31266
    ComverseInfosysG7231 = -24320
    ComverseInfosysAvqsbc = -24319
    ComverseInfosysSbc = -24318
    SymbolG729A = -24317
    VoiceageAmrWb = -24316
    IngenientG726 = -24315
    Mpeg4Aac = -24314
    EncoreG726 = -24313
    ZollAsao = -24312
    SpeexVoice = -24311
    VianixMasc = -24310
    Wm9SpectrumAnalyzer = -24309
    WmfSpectrumAnayzer = -24308
    Gsm610 = -24307
    Gsm620 = -24306
    Gsm660 = -24305
    Gsm690 = -24304
    GsmAdaptiveMultirateWb = -24303
    PolycomG722 = -24302
    PolycomG728 = -24301
    PolycomG729A = -24300
    PolycomSiren = -24299
    GlobalIpIlbc = -24298
    RadiotimeTimeShiftRadio = -24297
    NiceAca = -24296
    NiceAdpcm = -24295
    VocordG721 = -24294
    VocordG726 = -24293
    VocordG7221 = -24292
    VocordG728 = -24291
    VocordG729 = -24290
    VocordG729A = -24289
    VocordG7231 = -24288
    VocordLbc = -24287
    NiceG728 = -24286
    FraceTelecomG729 = -24285
    Codian = -24284
    Flac = -3668
    Extensible = -2
    Development = -1

class WaveFormatExtensible:
    Encoding: WaveFormatEncoding
    Channels: int
    SampleRate: int
    AverageBytesPerSecond: int
    BlockAlign: int
    BitsPerSample: int
    ExtraSize: int
    GuidSubFormat: Any
    ChannelMask: Speakers
    def __init__(self, rate: int, bits: int, channels: int) -> None: ...
    def ConvertLatencyToByteSize(self, milliseconds: int) -> int: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...
