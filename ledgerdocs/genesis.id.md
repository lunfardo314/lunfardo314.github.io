```
# Proxima ledger definitions
hash: 69097cea066a3b932f5f0c9a6e758be28b80b832aad195454eb64d83717d3284
functions:
# BEGIN EMBEDDED function definitions
#    function codes (opcodes) from 0 to 15 are reserved for predefined parameter access functions $i and $$i
# BEGIN SHORT EMBEDDED function definitions
#    function codes (opcodes) from 16 to 63 are reserved for 'SHORT EMBEDDED function codes'
   -
      sym: "fail"
      description: "fails with parameter as panic message, where '_' is replaced with space"
      funCode: 16
      numArgs: 1
      embedded: true
      short: true
   -
      sym: "slice"
      description: "slice($0,$1,$2) takes a slice of $0, from $1 to $2 inclusive. $1 and $2 must be 1-byte long"
      funCode: 17
      numArgs: 3
      embedded: true
      short: true
   -
      sym: "byte"
      description: "byte($0,$1) takes byte $1 of $0, returns 1-byte long slice. $1 must be 1-byte long"
      funCode: 18
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "tail"
      description: "tail($0,$1) returns slice of $0 from $1 to the end"
      funCode: 19
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "equal"
      description: "equal($0,$1) returns non-empty value if $0 and $1 are equal slices"
      funCode: 20
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "hasPrefix"
      description: "hasPrefix($0,$1) returns non-empty value if $0 has $1 as prefix"
      funCode: 21
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "len"
      description: "len($0)returns uint64 big-endian 8 bytes of the length of $0"
      funCode: 22
      numArgs: 1
      embedded: true
      short: true
   -
      sym: "not"
      description: "not($0) returns 0x if $0 is not empty, and non-empty value if $0 is empty"
      funCode: 23
      numArgs: 1
      embedded: true
      short: true
   -
      sym: "if"
      description: "if($0,$1,$2) returns eval value of $1 if $0 is non-empty and eval value of $1 otherwise"
      funCode: 24
      numArgs: 3
      embedded: true
      short: true
   -
      sym: "isZero"
      description: "isZero($0) returns 0x if $0 contains at least one non-zero byte"
      funCode: 25
      numArgs: 1
      embedded: true
      short: true
   -
      sym: "add"
      description: "add($0,$1) returns $0 + $1 as big-endian uint64. $0 and $1 is expanded to 8 bytes by adding leading 0-s"
      funCode: 26
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "sub"
      description: "sub($0,$1) returns $0 - $1 as big-endian uint64 or panics with 'underflow' if $0<$1. $0 and $1 is expanded to 8 bytes by adding leading 0-s"
      funCode: 27
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "mul"
      description: "mul($0,$1) returns $0 x $1 as big-endian uint64. $0 and $1 is expanded to 8 bytes by adding leading 0-s"
      funCode: 28
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "div"
      description: "div($0,$1) returns $0 / $1 (integer division) as big-endian uint64 or panics if $1 is 0. $0 and $1 is expanded to 8 bytes by adding leading 0-s"
      funCode: 29
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "mod"
      description: "mod($0,$1) returns $0 mod $1 as big-endian uint64 or panics if $1 is 0. $0 and $1 is expanded to 8 bytes by adding leading 0-s"
      funCode: 30
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "uint8Bytes"
      description: " expands $0 with leading 0-s up to 8 bytes"
      funCode: 31
      numArgs: 1
      embedded: true
      short: true
   -
      sym: "lessThan"
      description: "returns non-empty value of $0 < $1 lexicographically, otherwise returns 0x. Operands must be of equal length"
      funCode: 32
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "bitwiseOR"
      description: "bitwise OR operation on $0 and $1, which must have equal length"
      funCode: 33
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "bitwiseAND"
      description: "bitwise AND operation on $0 and $1, which must have equal length"
      funCode: 34
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "bitwiseNOT"
      description: "bitwise inversion of $0"
      funCode: 35
      numArgs: 1
      embedded: true
      short: true
   -
      sym: "bitwiseXOR"
      description: "bitwise XOR operation on $0 and $1, which must have equal length"
      funCode: 36
      numArgs: 2
      embedded: true
      short: true
   -
      sym: "at"
      description: "returns path in the transaction of the validity constraint being evaluated"
      funCode: 37
      numArgs: 0
      embedded: true
      short: true
   -
      sym: "atPath"
      description: "returns element of the transaction at path $0"
      funCode: 38
      numArgs: 1
      embedded: true
      short: true
# END SHORT EMBEDDED function definitions
# BEGIN LONG EMBEDDED function definitions
#    function codes (opcodes) from 64 to 318 are reserved for 'LONG EMBEDDED function codes'
   -
      sym: "concat"
      description: "concatenates variable number of arguments"
      funCode: 64
      numArgs: -1
      embedded: true
   -
      sym: "and"
      description: "returns non-empty value if all arguments are not empty, otherwise returns 0x"
      funCode: 65
      numArgs: -1
      embedded: true
   -
      sym: "or"
      description: "returns empty value 0x if all arguments are 0x (empty), otherwise returns non-empty value"
      funCode: 66
      numArgs: -1
      embedded: true
   -
      sym: "repeat"
      description: "repeat($0,$1) repeats $0 number of times $1. $1 must be 1-byte long"
      funCode: 67
      numArgs: 2
      embedded: true
   -
      sym: "firstCaseIndex"
      description: "evaluates one-by-one and returns first argument with non-empty value"
      funCode: 68
      numArgs: -1
      embedded: true
   -
      sym: "firstEqualIndex"
      description: "firstEqualIndex($0,$1,..$n) evaluates $0 and returns (i-1) of the parameter $i which is equal to $0"
      funCode: 69
      numArgs: -1
      embedded: true
   -
      sym: "selectCaseByIndex"
      description: "selectCaseByIndex($0,$1, ..$n) return value if the parameter based on the value of $0+1"
      funCode: 70
      numArgs: -1
      embedded: true
   -
      sym: "lshift64"
      description: "lshift64($0,$1) returns $0<<$1, where both arguments ar expanded to big-endian uint64 bytes by adding leading 0-s"
      funCode: 71
      numArgs: 2
      embedded: true
   -
      sym: "rshift64"
      description: "lshift64($0,$1) returns $0>>$1, where both arguments ar expanded to big-endian uint64 bytes by adding leading 0-s"
      funCode: 72
      numArgs: 2
      embedded: true
   -
      sym: "validSignatureED25519"
      description: "validSignatureED25519($0,$1,$2) returns non-empty value if $1 represents valid ED25519 signature of message $0 and  public key $2"
      funCode: 73
      numArgs: 3
      embedded: true
   -
      sym: "blake2b"
      description: "returns 32 bytes of the blake2b hash of the argument"
      funCode: 74
      numArgs: -1
      embedded: true
   -
      sym: "parseArgumentBytecode"
      description: "parseArgumentBytecode($0,$1,$2) treats $0 as bytecode. It check if its call prefix is equal to $1 and takes bytecode argument with index $2"
      funCode: 75
      numArgs: 3
      embedded: true
   -
      sym: "parsePrefixBytecode"
      description: "treats $0 as bytecode. Returns its call prefix"
      funCode: 76
      numArgs: 1
      embedded: true
   -
      sym: "parseInlineData"
      description: "treats $0 as bytecode of the inline data call. Strips the call prefix, returns the data"
      funCode: 77
      numArgs: 1
      embedded: true
   -
      sym: "callLocalLibrary"
      description: "calls local library"
      funCode: 78
      numArgs: -1
      embedded: true
   -
      sym: "atTuple8"
      description: "returns element of the serialized tuple at index $0 which must be 1 byte-long"
      funCode: 79
      numArgs: 2
      embedded: true
   -
      sym: "tupleLen"
      description: "returns number of elements of a tuple as 8 byte-long big-endian value"
      funCode: 80
      numArgs: 1
      embedded: true
   -
      sym: "ticksBefore"
      description: "number of ticks between timestamps $0 and $1 as big-endian uint64 if $0 is before $1, or 0x otherwise"
      funCode: 81
      numArgs: 2
      embedded: true
   -
      sym: "randomFromSeed"
      description: "uses $0 as seed to deterministically calculate a pseudo-random value. Returns 8-byte big-endian integer bytes in the interval [0,$1)"
      funCode: 82
      numArgs: 2
      embedded: true
# END LONG EMBEDDED function definitions
# BEGIN EXTENDED function definitions (defined by EasyFL formulas)
#    function codes (opcodes) from 319 and up to maximum 1022 are reserved for 'EXTENDED function codes'
   -
      sym: "false"
      description: "returns 0x"
      funCode: 319
      numArgs: 0
      bytecode: 80
      source: >
         0x         
         
   -
      sym: "true"
      description: "returns non-empty value"
      funCode: 320
      numArgs: 0
      bytecode: 81ff
      source: >
         0xff         
         
   -
      sym: "require"
      description: "equivalent to or($0,$1). Useful in context like require(<cond>, !!!fail_condition_not_satisfied)"
      funCode: 321
      numArgs: 2
      bytecode: 48420001
      source: >
         or($0,$1)         
         
   -
      sym: "lessOrEqualThan"
      description: "returns $0<=$1. Requires operands must be equal length"
      funCode: 322
      numArgs: 2
      bytecode: 4842200001140001
      source: >
         or(lessThan($0,$1),equal($0,$1))         
         
   -
      sym: "greaterThan"
      description: "returns $0>$1. Requires operands must be equal length"
      funCode: 323
      numArgs: 2
      bytecode: 1749420001
      source: >
         not(lessOrEqualThan($0,$1))         
         
   -
      sym: "greaterOrEqualThan"
      description: "returns $0>=$1. Requires operands must be equal length"
      funCode: 324
      numArgs: 2
      bytecode: 17200001
      source: >
         not(lessThan($0,$1))         
         
   -
      sym: "bytecode"
      description: "returns bytecode of the operand, i.e. arguments is compiled instead of evaluated"
      funCode: 325
      numArgs: 1
      bytecode: 08
      source: >
         $$0         
         
   -
      sym: "parseInlineDataArgument"
      description: "in bytecode $0, parses argument with index $2, treats it as inline data call, returns the inline data, Enforces call prefix is equal to $1"
      funCode: 326
      numArgs: 3
      bytecode: 444d4c4b000102
      source: >
         parseInlineData(parseArgumentBytecode($0,$1,$2))         
         
   -
      sym: "lessThanUint"
      description: "returns $0<$1 for arguments of any size <= 8. Each of arguments ar expanded fit leading 0-s up to 8 bytes and compare lexicographically"
      funCode: 327
      numArgs: 2
      bytecode: 201f001f01
      source: >
         lessThan(uint8Bytes($0), uint8Bytes($1))         
         
   -
      sym: "equalUint"
      description: "returns $0==$1 preliminary expanding each operand with leading 0-s to 8 bytes"
      funCode: 328
      numArgs: 2
      bytecode: 141f001f01
      source: >
         equal(uint8Bytes($0), uint8Bytes($1))         
         
   -
      sym: "max"
      description: "returns bigger one out of 2 operands of equal size"
      funCode: 329
      numArgs: 2
      bytecode: 182000010100
      source: >
         if(lessThan($0,$1),$1,$0)         
         
   -
      sym: "min"
      description: "returns smaller one out of 2 operands of equal size"
      funCode: 330
      numArgs: 2
      bytecode: 182000010001
      source: >
         if(lessThan($0,$1),$0,$1)         
         
   -
      sym: "constInitialSupply"
      description: "Initial number of tokens in the ledger"
      funCode: 331
      numArgs: 0
      bytecode: 8800038d7ea4c68000
      source: >
         u64/1000000000000000
   -
      sym: "constGenesisControllerPublicKey"
      description: "Public key ED25519 of the genesis controller in hexadecimal format"
      funCode: 332
      numArgs: 0
      bytecode: a09ad4caddd2356a7853eb038a5b4fd3197522af51af4073584260c53bbfaf1816
      source: >
         0x9ad4caddd2356a7853eb038a5b4fd3197522af51af4073584260c53bbfaf1816
   -
      sym: "constGenesisTimeUnix"
      description: "Unix time in seconds when ledger was initiated. Timestamp 0|0 corresponds to the genesis time"
      funCode: 333
      numArgs: 0
      bytecode: 88000000006841dc74
      source: >
         u64/1749146740
   -
      sym: "constTickDuration"
      description: "tick duration in nanoseconds. Default is 80ms"
      funCode: 334
      numArgs: 0
      bytecode: 880000000004c4b400
      source: >
         u64/80000000
   -
      sym: "constMaxTickValuePerSlot"
      description: "maximum value of ticks in the slot. Usually 127"
      funCode: 335
      numArgs: 0
      bytecode: 88000000000000007f
      source: >
         u64/127
   -
      sym: "ticksPerSlot64"
      description: "number of ticks in the slot. Usually 128"
      funCode: 336
      numArgs: 0
      bytecode: 1a414f880000000000000001
      source: >
         add(constMaxTickValuePerSlot, u64/1)
   -
      sym: "constSlotInflationBase"
      description: "maximum inflation of the total supply in slot 0. Usually 33000000"
      funCode: 337
      numArgs: 0
      bytecode: 880000000001f78a40
      source: >
         u64/33000000
   -
      sym: "constLinearInflationSlots"
      description: "number of slot with linear inflation"
      funCode: 338
      numArgs: 0
      bytecode: 880000000000000003
      source: >
         u64/3
   -
      sym: "constBranchInflationBonusBase"
      description: "maximum value of the branch inflation bonus. Usually 5000000"
      funCode: 339
      numArgs: 0
      bytecode: 8800000000004c4b40
      source: >
         u64/5000000
   -
      sym: "constMinimumAmountOnSequencer"
      description: "minimum amount of tokens on the sequencer output. For testnet it is 1000 * PRXI = 1000000000"
      funCode: 340
      numArgs: 0
      bytecode: 88000000003b9aca00
      source: >
         u64/1000000000
   -
      sym: "constMaxNumberOfEndorsements"
      description: "up to 8 endorsements"
      funCode: 341
      numArgs: 0
      bytecode: 880000000000000008
      source: >
         u64/8
   -
      sym: "constPreBranchConsolidationTicks"
      description: "number of last ticks in a slot when sequencer transaction cannot consume more than 2 UTXOs"
      funCode: 342
      numArgs: 0
      bytecode: 880000000000000019
      source: >
         u64/25
   -
      sym: "constPostBranchConsolidationTicks"
      description: "number of first ticks in the timestamp of the sequencer transaction"
      funCode: 343
      numArgs: 0
      bytecode: 88000000000000000c
      source: >
         u64/12
   -
      sym: "constTransactionPace"
      description: "minimum number of ticks between non-sequencer transaction and its inputs"
      funCode: 344
      numArgs: 0
      bytecode: 88000000000000000c
      source: >
         u64/12
   -
      sym: "constTransactionPaceSequencer"
      description: "minimum number of ticks between sequencer transaction and its inputs and endorsed transactions"
      funCode: 345
      numArgs: 0
      bytecode: 880000000000000002
      source: >
         u64/2
   -
      sym: "constVBCost16"
      description: "constant for the storage deposit constraint"
      funCode: 346
      numArgs: 0
      bytecode: 820001
      source: >
         u16/1
   -
      sym: "constDescription"
      description: "arbitrary binary data"
      funCode: 347
      numArgs: 0
      bytecode: 9a50726f78696d61206c656467657220646566696e6974696f6e73
      source: >
         0x50726f78696d61206c656467657220646566696e6974696f6e73
   -
      sym: "timeSlotSizeBytes"
      description: "constant for the storage deposit constraint"
      funCode: 348
      numArgs: 0
      bytecode: 8104
      source: >
         4
   -
      sym: "timestampByteSize"
      description: "constant for the storage deposit constraint"
      funCode: 349
      numArgs: 0
      bytecode: 8105
      source: >
         5
   -
      sym: "pathToTransaction"
      funCode: 350
      numArgs: 0
      bytecode: 8100
      source: >
         0
   -
      sym: "pathToConsumedOutputs"
      funCode: 351
      numArgs: 0
      bytecode: 820100
      source: >
         0x0100
   -
      sym: "pathToProducedOutputs"
      funCode: 352
      numArgs: 0
      bytecode: 820002
      source: >
         0x0002
   -
      sym: "pathToUnlockParams"
      funCode: 353
      numArgs: 0
      bytecode: 820001
      source: >
         0x0001
   -
      sym: "pathToInputIDs"
      funCode: 354
      numArgs: 0
      bytecode: 820000
      source: >
         0x0000
   -
      sym: "pathToSignature"
      funCode: 355
      numArgs: 0
      bytecode: 820003
      source: >
         0x0003
   -
      sym: "pathToSeqAndStemOutputIndices"
      funCode: 356
      numArgs: 0
      bytecode: 820004
      source: >
         0x0004
   -
      sym: "pathToInputCommitment"
      funCode: 357
      numArgs: 0
      bytecode: 820007
      source: >
         0x0007
   -
      sym: "pathToEndorsements"
      funCode: 358
      numArgs: 0
      bytecode: 820008
      source: >
         0x0008
   -
      sym: "pathToExplicitBaseline"
      funCode: 359
      numArgs: 0
      bytecode: 820009
      source: >
         0x0009
   -
      sym: "pathToTimestamp"
      funCode: 360
      numArgs: 0
      bytecode: 820005
      source: >
         0x0005
   -
      sym: "pathToTotalProducedAmount"
      funCode: 361
      numArgs: 0
      bytecode: 820006
      source: >
         0x0006
   -
      sym: "pathToLocalLibraries"
      funCode: 362
      numArgs: 0
      bytecode: 82000a
      source: >
         0x000a
   -
      sym: "amountConstraintIndex"
      funCode: 363
      numArgs: 0
      bytecode: 8100
      source: >
         0
   -
      sym: "lockConstraintIndex"
      funCode: 364
      numArgs: 0
      bytecode: 8101
      source: >
         1
   -
      sym: "mustSize"
      funCode: 365
      numArgs: 2
      bytecode: 18494816000100108f77726f6e6720646174612073697a65
      source: >
         if(equalUint(len($0), $1), $0, !!!wrong_data_size)
   -
      sym: "mustValidTimeTick"
      funCode: 366
      numArgs: 1
      bytecode: 184841494816008101201f00414f00109177726f6e67207469636b732076616c7565
      source: >
         if(and(equalUint(len($0),1), lessThan(uint8Bytes($0),constMaxTickValuePerSlot) ), $0, !!!wrong_ticks_value)
   -
      sym: "mustValidTimeSlot"
      description: "returns $0 result if $0 can be interpreted as slot value, otherwise returns 0x"
      funCode: 367
      numArgs: 1
      bytecode: 1849481600415c00108f77726f6e6720736c6f742064617461
      source: >
         if(equalUint(len($0), timeSlotSizeBytes), $0, !!!wrong_slot_data)
   -
      sym: "mul8"
      description: "last byte of big-endian uint64 multiplication result"
      funCode: 368
      numArgs: 2
      bytecode: 121c00018107
      source: >
         byte(mul($0,$1),7)
   -
      sym: "div8"
      description: "last byte of big-endian uint64 integer division result"
      funCode: 369
      numArgs: 2
      bytecode: 121d00018107
      source: >
         byte(div($0,$1),7)
   -
      sym: "timestampBytes"
      description: "validates and composes $0 as slot value and $1 as ticks value into timestamp"
      funCode: 370
      numArgs: 2
      bytecode: 4840456f004970456e018102
      source: >
         concat(mustValidTimeSlot($0),mul8(mustValidTimeTick($1),2))
   -
      sym: "first4Bytes"
      description: "first 4 bytes of $0"
      funCode: 371
      numArgs: 1
      bytecode: 110081008103
      source: >
         slice($0, 0, 3)
   -
      sym: "first5Bytes"
      description: "first 5 bytes of $0"
      funCode: 372
      numArgs: 1
      bytecode: 110081008104
      source: >
         slice($0, 0, 4)
   -
      sym: "timestampBytesFromPrefix"
      description: "nullifies sequencer bit in the prefix and thus makes a timestamp from a txid"
      funCode: 373
      numArgs: 1
      bytecode: 2245740085fffffffff6
      source: >
         bitwiseAND(first5Bytes($0), 0xfffffffff6)
   -
      sym: "timeTickFromTimestampBytes"
      description: "returns ticks of the timestamp"
      funCode: 374
      numArgs: 1
      bytecode: 4971120081048102
      source: >
         div8(byte($0, 4),2)
   -
      sym: "isTimestampBytesOnSlotBoundary"
      description: "returns non-empty value if ticks of the $0 timestamp are 0"
      funCode: 375
      numArgs: 1
      bytecode: 19457600
      source: >
         isZero(timeTickFromTimestampBytes($0))
   -
      sym: "amountConstraint"
      funCode: 376
      numArgs: 1
      bytecode: 484f00416b
      source: >
         atTuple8($0, amountConstraintIndex)
   -
      sym: "lockConstraint"
      funCode: 377
      numArgs: 1
      bytecode: 484f00416c
      source: >
         atTuple8($0, lockConstraintIndex)
   -
      sym: "isPathToConsumedOutput"
      funCode: 378
      numArgs: 1
      bytecode: 1500415f
      source: >
         hasPrefix($0, pathToConsumedOutputs)
   -
      sym: "isPathToProducedOutput"
      funCode: 379
      numArgs: 1
      bytecode: 15004160
      source: >
         hasPrefix($0, pathToProducedOutputs)
   -
      sym: "consumedOutputPathByIndex"
      funCode: 380
      numArgs: 1
      bytecode: 4840415f00
      source: >
         concat(pathToConsumedOutputs,$0)
   -
      sym: "unlockParamsPathByIndex"
      funCode: 381
      numArgs: 1
      bytecode: 4840416100
      source: >
         concat(pathToUnlockParams,$0)
   -
      sym: "producedOutputPathByIndex"
      funCode: 382
      numArgs: 1
      bytecode: 4840416000
      source: >
         concat(pathToProducedOutputs,$0)
   -
      sym: "consumedOutputByIndex"
      funCode: 383
      numArgs: 1
      bytecode: 26457c00
      source: >
         atPath(consumedOutputPathByIndex($0))
   -
      sym: "unlockParamsByIndex"
      funCode: 384
      numArgs: 1
      bytecode: 26457d00
      source: >
         atPath(unlockParamsPathByIndex($0))
   -
      sym: "producedOutputByIndex"
      funCode: 385
      numArgs: 1
      bytecode: 26457e00
      source: >
         atPath(producedOutputPathByIndex($0))
   -
      sym: "producedConstraintByIndex"
      funCode: 386
      numArgs: 1
      bytecode: 484f45811200810012008101
      source: >
         atTuple8(producedOutputByIndex(byte($0,0)), byte($0,1))
   -
      sym: "consumedConstraintByIndex"
      funCode: 387
      numArgs: 1
      bytecode: 484f457f1200810012008101
      source: >
         atTuple8(consumedOutputByIndex(byte($0,0)), byte($0,1))
   -
      sym: "unlockParamsByConstraintIndex"
      funCode: 388
      numArgs: 1
      bytecode: 484f45801200810012008101
      source: >
         atTuple8(unlockParamsByIndex(byte($0,0)), byte($0,1))
   -
      sym: "consumedLockByInputIndex"
      funCode: 389
      numArgs: 1
      bytecode: 4583484000416c
      source: >
         consumedConstraintByIndex(concat($0, lockConstraintIndex))
   -
      sym: "inputIDByIndex"
      funCode: 390
      numArgs: 1
      bytecode: 264840416200
      source: >
         atPath(concat(pathToInputIDs,$0))
   -
      sym: "timestampOfInputByIndex"
      funCode: 391
      numArgs: 1
      bytecode: 4575458600
      source: >
         timestampBytesFromPrefix(inputIDByIndex($0))
   -
      sym: "timeSlotOfInputByIndex"
      funCode: 392
      numArgs: 1
      bytecode: 4573458600
      source: >
         first4Bytes(inputIDByIndex($0))
   -
      sym: "txBytes"
      funCode: 393
      numArgs: 0
      bytecode: 26415e
      source: >
         atPath(pathToTransaction)
   -
      sym: "txSignature"
      funCode: 394
      numArgs: 0
      bytecode: 264163
      source: >
         atPath(pathToSignature)
   -
      sym: "txTimestampBytes"
      funCode: 395
      numArgs: 0
      bytecode: 264168
      source: >
         atPath(pathToTimestamp)
   -
      sym: "txExplicitBaseline"
      funCode: 396
      numArgs: 0
      bytecode: 264167
      source: >
         atPath(pathToExplicitBaseline)
   -
      sym: "txTotalProducedAmount"
      funCode: 397
      numArgs: 0
      bytecode: 1f264169
      source: >
         uint8Bytes(atPath(pathToTotalProducedAmount))
   -
      sym: "txTimeSlot"
      funCode: 398
      numArgs: 0
      bytecode: 4573418b
      source: >
         first4Bytes(txTimestampBytes)
   -
      sym: "txTimeTick"
      funCode: 399
      numArgs: 0
      bytecode: 4576418b
      source: >
         timeTickFromTimestampBytes(txTimestampBytes)
   -
      sym: "txSequencerOutputIndex"
      funCode: 400
      numArgs: 0
      bytecode: 122641648100
      source: >
         byte(atPath(pathToSeqAndStemOutputIndices), 0)
   -
      sym: "txStemOutputIndex"
      funCode: 401
      numArgs: 0
      bytecode: 122641648101
      source: >
         byte(atPath(pathToSeqAndStemOutputIndices), 1)
   -
      sym: "sequencerFlagON"
      funCode: 402
      numArgs: 1
      bytecode: 171922120081048101
      source: >
         not(isZero(bitwiseAND(byte($0,4),0x01)))
   -
      sym: "isSequencerTransaction"
      funCode: 403
      numArgs: 0
      bytecode: 1714419081ff
      source: >
         not(equal(txSequencerOutputIndex, 0xff))
   -
      sym: "isBranchTransaction"
      funCode: 404
      numArgs: 0
      bytecode: 484141931714419181ff
      source: >
         and(isSequencerTransaction, not(equal(txStemOutputIndex, 0xff)))
   -
      sym: "numEndorsements"
      funCode: 405
      numArgs: 0
      bytecode: 4450264166
      source: >
         tupleLen(atPath(pathToEndorsements))
   -
      sym: "numInputs"
      funCode: 406
      numArgs: 0
      bytecode: 4450264162
      source: >
         tupleLen(atPath(pathToInputIDs))
   -
      sym: "numProducedOutputs"
      funCode: 407
      numArgs: 0
      bytecode: 4450264160
      source: >
         tupleLen(atPath(pathToProducedOutputs))
   -
      sym: "txEssenceBytes"
      funCode: 408
      numArgs: 0
      bytecode: 48405440264162264161264160264164264168544026416926416526416626416726416a
      source: >
          concat( concat( atPath(pathToInputIDs), atPath(pathToUnlockParams), atPath(pathToProducedOutputs), atPath(pathToSeqAndStemOutputIndices), atPath(pathToTimestamp) ), concat( atPath(pathToTotalProducedAmount), atPath(pathToInputCommitment), atPath(pathToEndorsements), atPath(pathToExplicitBaseline), atPath(pathToLocalLibraries) ) )
   -
      sym: "txIDPrefix"
      funCode: 409
      numArgs: 0
      bytecode: 18419321418b850000000001418b
      source: >
         if(isSequencerTransaction, bitwiseOR(txTimestampBytes, 0x0000000001), txTimestampBytes)
   -
      sym: "txID"
      funCode: 410
      numArgs: 0
      bytecode: 4c404199121b41978101810711444a41988106811f
      source: >
         concat(txIDPrefix, byte(sub(numProducedOutputs,1), 7), slice(blake2b(txEssenceBytes),6,31))
   -
      sym: "selfOutputPath"
      funCode: 411
      numArgs: 0
      bytecode: 112581008102
      source: >
         slice(at,0,2)
   -
      sym: "selfSiblingConstraint"
      funCode: 412
      numArgs: 1
      bytecode: 484f26419b00
      source: >
         atTuple8(atPath(selfOutputPath), $0)
   -
      sym: "selfOutputBytes"
      funCode: 413
      numArgs: 0
      bytecode: 26419b
      source: >
         atPath(selfOutputPath)
   -
      sym: "selfNumConstraints"
      funCode: 414
      numArgs: 0
      bytecode: 4450419d
      source: >
         tupleLen(selfOutputBytes)
   -
      sym: "self"
      funCode: 415
      numArgs: 0
      bytecode: 2625
      source: >
         atPath(at)
   -
      sym: "selfBytecodePrefix"
      funCode: 416
      numArgs: 0
      bytecode: 444c419f
      source: >
         parsePrefixBytecode(self)
   -
      sym: "selfIsConsumedOutput"
      funCode: 417
      numArgs: 0
      bytecode: 457a25
      source: >
         isPathToConsumedOutput(at)
   -
      sym: "selfIsProducedOutput"
      funCode: 418
      numArgs: 0
      bytecode: 457b25
      source: >
         isPathToProducedOutput(at)
   -
      sym: "selfOutputIndex"
      funCode: 419
      numArgs: 0
      bytecode: 12258102
      source: >
         byte(at, 2)
   -
      sym: "selfBlockIndex"
      funCode: 420
      numArgs: 0
      bytecode: 13258103
      source: >
         tail(at, 3)
   -
      sym: "selfBranch"
      funCode: 421
      numArgs: 0
      bytecode: 112581008101
      source: >
         slice(at,0,1)
   -
      sym: "selfConstraintIndex"
      funCode: 422
      numArgs: 0
      bytecode: 112581028103
      source: >
         slice(at, 2, 3)
   -
      sym: "constraintData"
      funCode: 423
      numArgs: 1
      bytecode: 13008101
      source: >
         tail($0,1)
   -
      sym: "selfConstraintData"
      funCode: 424
      numArgs: 0
      bytecode: 45a7419f
      source: >
         constraintData(self)
   -
      sym: "selfUnlockParameters"
      funCode: 425
      numArgs: 0
      bytecode: 264840416141a6
      source: >
         atPath(concat(pathToUnlockParams, selfConstraintIndex))
   -
      sym: "selfReferencedPath"
      funCode: 426
      numArgs: 0
      bytecode: 4c4041a541a941a4
      source: >
         concat(selfBranch, selfUnlockParameters, selfBlockIndex)
   -
      sym: "selfSiblingUnlockBlock"
      funCode: 427
      numArgs: 1
      bytecode: 484f264840416141a300
      source: >
         atTuple8(atPath(concat(pathToUnlockParams, selfOutputIndex)), $0)
   -
      sym: "selfHashUnlock"
      funCode: 428
      numArgs: 1
      bytecode: 181400444a41a941a980
      source: >
         if(equal($0, blake2b(selfUnlockParameters)),selfUnlockParameters,nil)
   -
      sym: "signatureED25519"
      funCode: 429
      numArgs: 1
      bytecode: 11008100813f
      source: >
         slice($0, 0, 63)
   -
      sym: "publicKeyED25519"
      funCode: 430
      numArgs: 1
      bytecode: 11008140815f
      source: >
         slice($0, 64, 95)
   -
      sym: "_adjustedDiffSlots"
      funCode: 431
      numArgs: 2
      bytecode: 1a1b45730145730018457700880000000000000001880000000000000000
      source: >
         add(sub(first4Bytes($1),first4Bytes($0)),if(isTimestampBytesOnSlotBoundary($0),u64/1,u64/0))
   -
      sym: "_baseInflation"
      funCode: 432
      numArgs: 2
      bytecode: 1d011a1d414b4151457300
      source: >
         div($1,add(div(constInitialSupply,constSlotInflationBase),first4Bytes($0)))
   -
      sym: "_calcChainInflationAmount"
      funCode: 433
      numArgs: 3
      bytecode: 18204152011c415249b000021c0149b00002
      source: >
         if(lessThan(constLinearInflationSlots,$1),mul(constLinearInflationSlots,_baseInflation($0,$2)),mul($1,_baseInflation($0,$2)))
   -
      sym: "calcChainInflationAmount"
      funCode: 434
      numArgs: 3
      bytecode: 181720000110b063616c63436861696e496e666c6174696f6e416d6f756e74206661696c65642077726f6e672074696d657374616d7073184577018800000000000000004db10049af000102
      source: >
         if(not(lessThan($0,$1)),!!!calcChainInflationAmount_failed_wrong_timestamps,if(isTimestampBytesOnSlotBoundary($1),u64/0,_calcChainInflationAmount($0,_adjustedDiffSlots($0,$1),$2)))
   -
      sym: "branchInflationBonusFromRandomnessProof"
      funCode: 435
      numArgs: 1
      bytecode: 1a48520041538101
      source: >
         add(randomFromSeed($0,constBranchInflationBonusBase),1)
   -
      sym: "amount"
      funCode: 436
      numArgs: 1
      bytecode: 494148411441a481004942160088000000000000000810b4616d6f756e7420636f6e73747261696e74206d75737420626520617420696e646578203020616e64206c656e20617267303c3d38
      source: >
         require(and(equal(selfBlockIndex,0),lessOrEqualThan(len($0),u64/8)),!!!amount_constraint_must_be_at_index_0_and_len_arg0<=8)
   -
      sym: "amountValue"
      funCode: 437
      numArgs: 1
      bytecode: 1f4d46484f00416b8245b48100
      source: >
         uint8Bytes(parseInlineDataArgument(atTuple8($0,amountConstraintIndex),#amount,0))
   -
      sym: "selfAmountValue"
      funCode: 438
      numArgs: 0
      bytecode: 45b5419d
      source: >
         amountValue(selfOutputBytes)
   -
      sym: "storageDeposit"
      funCode: 439
      numArgs: 1
      bytecode: 1c415a00
      source: >
         mul(constVBCost16,$0)
   -
      sym: "selfMustStandardAmount"
      funCode: 440
      numArgs: 0
      bytecode: 4941172041b645b716419d10b0616d6f756e74206f6e206f757470757420697320736d616c6c6572207468616e20616c6c6f776564206d696e696d756d
      source: >
         require(not(lessThan(selfAmountValue,storageDeposit(len(selfOutputBytes)))),!!!amount_on_output_is_smaller_than_allowed_minimum)
   -
      sym: "unlockedWithSigED25519"
      funCode: 441
      numArgs: 3
      bytecode: 48411400444a024c49419a0102
      source: >
         and(equal($0,blake2b($2)),validSignatureED25519(txID,$1,$2))
   -
      sym: "unlockedByReference"
      funCode: 442
      numArgs: 1
      bytecode: 4c41141600880000000000000001200041a314419f458500
      source: >
         and(equal(len($0),u64/1),lessThan($0,selfOutputIndex),equal(self,consumedLockByInputIndex($0)))
   -
      sym: "addressED25519"
      funCode: 443
      numArgs: 1
      bytecode: 4c4149411441a4810110986c6f636b73206d75737420626520617420626c6f636b203141b84842484141a2141600880000000000000020484141a1484245ba41a94db90045ad418a45ae418a
      source: >
         and(require(equal(selfBlockIndex,1),!!!locks_must_be_at_block_1),selfMustStandardAmount,or(and(selfIsProducedOutput,equal(len($0),u64/32)),and(selfIsConsumedOutput,or(unlockedByReference(selfUnlockParameters),unlockedWithSigED25519($0,signatureED25519(txSignature),publicKeyED25519(txSignature))))))
   -
      sym: "a"
      funCode: 444
      numArgs: 1
      bytecode: 45bb00
      source: >
         addressED25519($0)
   -
      sym: "conditionalLock"
      funCode: 445
      numArgs: 8
      bytecode: 544650440002040601030507
      source: >
         selectCaseByIndex(firstCaseIndex($0,$2,$4,$6),$1,$3,$5,$7)
   -
      sym: "deadlineLock"
      funCode: 446
      numArgs: 3
      bytecode: 1841a161bd2000418e01172000418e0280808080456f00
      source: >
         if(selfIsConsumedOutput,conditionalLock(lessThan($0,txTimeSlot),$1,not(lessThan($0,txTimeSlot)),$2,0x,0x,0x,0x),mustValidTimeSlot($0))
   -
      sym: "timelock"
      funCode: 447
      numArgs: 1
      bytecode: 4841456f00484241a2484141a1494200418e
      source: >
         and(mustValidTimeSlot($0),or(selfIsProducedOutput,and(selfIsConsumedOutput,lessOrEqualThan($0,txTimeSlot))))
   -
      sym: "originChainData"
      funCode: 448
      numArgs: 0
      bytecode: 484048438100812083ffffff
      source: >
         concat(repeat(0,32),0xffffff)
   -
      sym: "destroyUnlockParams"
      funCode: 449
      numArgs: 0
      bytecode: 83ffffff
      source: >
         0xffffff
   -
      sym: "chainID"
      funCode: 450
      numArgs: 1
      bytecode: 11008100811f
      source: >
         slice($0,0,31)
   -
      sym: "transitionMode"
      funCode: 451
      numArgs: 1
      bytecode: 12008122
      source: >
         byte($0,34)
   -
      sym: "predecessorConstraintIndex"
      funCode: 452
      numArgs: 1
      bytecode: 110081208121
      source: >
         slice($0,32,33)
   -
      sym: "validPredecessorData"
      funCode: 453
      numArgs: 2
      bytecode: 4841181945c2014841140141c01445c200444a45861200812044411445c20045c2011445c30012458445c4008102
      source: >
         and(if(isZero(chainID($1)),and(equal($1,originChainData),equal(chainID($0),blake2b(inputIDByIndex(byte($0,32))))),and(equal(chainID($0),chainID($1)),)),equal(transitionMode($0),byte(unlockParamsByConstraintIndex(predecessorConstraintIndex($0)),2)))
   -
      sym: "chainPredecessorData"
      funCode: 454
      numArgs: 1
      bytecode: 4d4645830041a08100
      source: >
         parseInlineDataArgument(consumedConstraintByIndex($0),selfBytecodePrefix,0)
   -
      sym: "validSuccessorData"
      funCode: 455
      numArgs: 2
      bytecode: 4841181945c200140041c01445c20045c2011445c40141a6
      source: >
         and(if(isZero(chainID($0)),equal($0,originChainData),equal(chainID($0),chainID($1))),equal(predecessorConstraintIndex($1),selfConstraintIndex))
   -
      sym: "chainSuccessorData"
      funCode: 456
      numArgs: 0
      bytecode: 4d4645821141a98100810141a08100
      source: >
         parseInlineDataArgument(producedConstraintByIndex(slice(selfUnlockParameters,0,1)),selfBytecodePrefix,0)
   -
      sym: "chain"
      funCode: 457
      numArgs: 1
      bytecode: 4841171441a381ff50421848411945c20041a24842140041c01092636861696e2077726f6e67206f726967696e80484141a14c421441a941c149c70041c81095636861696e2077726f6e6720737563636573736f72484141a2484249c50045c645c4001097636861696e2077726f6e67207072656465636573736f721097636861696e20636f6e73747261696e74206661696c6564
      source: >
         and(not(equal(selfOutputIndex,0xff)),or(if(and(isZero(chainID($0)),selfIsProducedOutput),or(equal($0,originChainData),!!!chain_wrong_origin),nil),and(selfIsConsumedOutput,or(equal(selfUnlockParameters,destroyUnlockParams),validSuccessorData($0,chainSuccessorData),!!!chain_wrong_successor)),and(selfIsProducedOutput,or(validPredecessorData($0,chainPredecessorData(predecessorConstraintIndex($0))),!!!chain_wrong_predecessor)),!!!chain_constraint_failed))
   -
      sym: "selfChainData"
      funCode: 458
      numArgs: 1
      bytecode: 4d46459c008245c98100
      source: >
         parseInlineDataArgument(selfSiblingConstraint($0),#chain,0)
   -
      sym: "selfChainPredecessorInputIndex"
      funCode: 459
      numArgs: 1
      bytecode: 1245ca008120
      source: >
         byte(selfChainData($0),32)
   -
      sym: "selfChainPredecessorTimestamp"
      funCode: 460
      numArgs: 1
      bytecode: 458745cb00
      source: >
         timestampOfInputByIndex(selfChainPredecessorInputIndex($0))
   -
      sym: "producedStemLockOfSelfTx"
      funCode: 461
      numArgs: 0
      bytecode: 457945814191
      source: >
         lockConstraint(producedOutputByIndex(txStemOutputIndex))
   -
      sym: "_predOutputIDOnSuccessor"
      funCode: 462
      numArgs: 0
      bytecode: 4d4641cd41a08100
      source: >
         parseInlineDataArgument(producedStemLockOfSelfTx,selfBytecodePrefix,0)
   -
      sym: "_vrfProofOnSuccessor"
      funCode: 463
      numArgs: 0
      bytecode: 4d4641cd41a08101
      source: >
         parseInlineDataArgument(producedStemLockOfSelfTx,selfBytecodePrefix,1)
   -
      sym: "_predVRFProof"
      funCode: 464
      numArgs: 1
      bytecode: 4d464583484000810141a08101
      source: >
         parseInlineDataArgument(consumedConstraintByIndex(concat($0,1)),selfBytecodePrefix,1)
   -
      sym: "stemLock"
      funCode: 465
      numArgs: 2
      bytecode: 584149414194109c6d7573742062652061206272616e6368207472616e73616374696f6e49414948419e810210ae7374656d206f7574707574206d75737420636f6e7461696e2065786163746c79203220636f6e73747261696e747349411441a4810110986c6f636b73206d75737420626520617420626c6f636b203149411941b61093616d6f756e74206d757374206265207a65726f496d00812148424c4141a1494114458641a341ce10ad77726f6e67207374656d207072656465636573736f72206f7574707574204944206f6e20737563636573736f7249414c49484001418e41cf45ae418a10965652462070726f6f6620636865636b206661696c6564484141a21441a34191
      source: >
         and(require(isBranchTransaction,!!!must_be_a_branch_transaction),require(equalUint(selfNumConstraints,2),!!!stem_output_must_contain_exactly_2_constraints),require(equal(selfBlockIndex,1),!!!locks_must_be_at_block_1),require(isZero(selfAmountValue),!!!amount_must_be_zero),mustSize($0,33),or(and(selfIsConsumedOutput,require(equal(inputIDByIndex(selfOutputIndex),_predOutputIDOnSuccessor),!!!wrong_stem_predecessor_output_ID_on_successor),require(validSignatureED25519(concat($1,txTimeSlot),_vrfProofOnSuccessor,publicKeyED25519(txSignature)),!!!VRF_proof_check_failed)),and(selfIsProducedOutput,equal(selfOutputIndex,txStemOutputIndex))))
   -
      sym: "mustMinimumAmountOnSequencer"
      funCode: 466
      numArgs: 0
      bytecode: 4941172041b6415410aa6d696e696d756d2073657175656e63657220616d6f756e7420636f6e73747261696e74206661696c6564
      source: >
         require(not(lessThan(selfAmountValue,constMinimumAmountOnSequencer)),!!!minimum_sequencer_amount_constraint_failed)
   -
      sym: "_inputSameSlot"
      funCode: 467
      numArgs: 1
      bytecode: 14418e458800
      source: >
         equal(txTimeSlot,timeSlotOfInputByIndex($0))
   -
      sym: "_noChainPredecessorCase"
      funCode: 468
      numArgs: 0
      bytecode: 4841494117419410b573657175656e63657220636861696e206f726967696e2063616e2774206265206f6e206272616e6368207472616e73616374696f6e49411719419510c173657175656e63657220636861696e206f726967696e206d75737420656e646f72736520616e6f746865722073657175656e636572207472616e73616374696f6e
      source: >
         and(require(not(isBranchTransaction),!!!sequencer_chain_origin_can't_be_on_branch_transaction),require(not(isZero(numEndorsements)),!!!sequencer_chain_origin_must_endorse_another_sequencer_transaction))
   -
      sym: "_sameSlotPredecessorCase"
      funCode: 469
      numArgs: 1
      bytecode: 4941484245924586001719419510ee73657175656e63657220636861696e207072656465636573736f72206f6e207468652073616d6520736c6f74206d7573742062652065697468657220612073657175656e63657220747820746f6f206f7220656e646f72736520616e6f746865722073657175656e636572207478
      source: >
         require(or(sequencerFlagON(inputIDByIndex($0)),not(isZero(numEndorsements))),!!!sequencer_chain_predecessor_on_the_same_slot_must_be_either_a_sequencer_tx_too_or_endorse_another_sequencer_tx)
   -
      sym: "_crossSlotPredecessorCase"
      funCode: 470
      numArgs: 0
      bytecode: 49414c424194171941951719418c10d973657175656e6365722074782068617320696e636f72726563742063726f737320736c6f7420636861696e207072656465636573736f72206f7220646f6573206e6f74206861766520616e7920656e646f7273656d656e7473
      source: >
         require(or(isBranchTransaction,not(isZero(numEndorsements)),not(isZero(txExplicitBaseline))),!!!sequencer_tx_has_incorrect_cross_slot_chain_predecessor_or_does_not_have_any_endorsements)
   -
      sym: "_sequencer"
      funCode: 471
      numArgs: 1
      bytecode: 4c424841140081ff41d4484145d30045d50048411745d30041d6
      source: >
         or(and(equal($0,0xff),_noChainPredecessorCase),and(_inputSameSlot($0),_sameSlotPredecessorCase($0)),and(not(_inputSameSlot($0)),_crossSlotPredecessorCase))
   -
      sym: "zeroTickOnBranchOnly"
      funCode: 472
      numArgs: 0
      bytecode: 48421719418f4194
      source: >
         or(not(isZero(txTimeTick)),isBranchTransaction)
   -
      sym: "checkPreBranchConsolidationTicks"
      funCode: 473
      numArgs: 0
      bytecode: 4842144196880000000000000001494149421f418f1b414f415610c873657175656e636572207472616e73616374696f6e2076696f6c61746573207072652d6272616e636820636f6e736f6c69646174696f6e207469636b7320636f6e73747261696e74
      source: >
         or(equal(numInputs,u64/1),require(lessOrEqualThan(uint8Bytes(txTimeTick),sub(constMaxTickValuePerSlot,constPreBranchConsolidationTicks)),!!!sequencer_transaction_violates_pre-branch_consolidation_ticks_constraint))
   -
      sym: "checkPostBranchConsolidationTicks"
      funCode: 474
      numArgs: 0
      bytecode: 494148424194494241571f418f10c973657175656e636572207472616e73616374696f6e2076696f6c6174657320706f7374206272616e636820636f6e736f6c69646174696f6e207469636b7320636f6e73747261696e74
      source: >
         require(or(isBranchTransaction,lessOrEqualThan(constPostBranchConsolidationTicks,uint8Bytes(txTimeTick))),!!!sequencer_transaction_violates_post_branch_consolidation_ticks_constraint)
   -
      sym: "sequencer"
      funCode: 475
      numArgs: 2
      bytecode: 4c41496d00810141d2484241a160414941171441a381ff10a773657175656e636572206f75747075742063616e277420626520617420696e646578203078666649411441a3419010b2696e636f6e73697374656e742073657175656e636572206f757470757420696e646578206f6e207472616e73616374696f6e494117140081ff10a9636861696e20636f6e73747261696e7420696e6465782030786666206973206e6f7420616c6f776564494141d810b96e6f6e2d6272616e63682073657175656e636572207472616e73616374696f6e2063616e74206265206f6e20736c6f7420626f756e646172794941141f01418d10a677726f6e6720746f74616c20616d6f756e74206f6e2073657175656e636572206f757470757441d941da45d745cb00
      source: >
         and(mustSize($0,1),mustMinimumAmountOnSequencer,or(selfIsConsumedOutput,and(require(not(equal(selfOutputIndex,0xff)),!!!sequencer_output_can't_be_at_index_0xff),require(equal(selfOutputIndex,txSequencerOutputIndex),!!!inconsistent_sequencer_output_index_on_transaction),require(not(equal($0,0xff)),!!!chain_constraint_index_0xff_is_not_alowed),require(zeroTickOnBranchOnly,!!!non-branch_sequencer_transaction_cant_be_on_slot_boundary),require(equal(uint8Bytes($1),txTotalProducedAmount),!!!wrong_total_amount_on_sequencer_output),checkPreBranchConsolidationTicks,checkPostBranchConsolidationTicks,_sequencer(selfChainPredecessorInputIndex($0)))))
   -
      sym: "_producedVRFProof"
      funCode: 476
      numArgs: 0
      bytecode: 4d46458248404191416c8249d18101
      source: >
         parseInlineDataArgument(producedConstraintByIndex(concat(txStemOutputIndex,lockConstraintIndex)),#stemLock,1)
   -
      sym: "_calcChainInflationAmountForPredecessor"
      funCode: 477
      numArgs: 1
      bytecode: 4db2458700418b45b5457f00
      source: >
         calcChainInflationAmount(timestampOfInputByIndex($0),txTimestampBytes,amountValue(consumedOutputByIndex($0)),)
   -
      sym: "inflation"
      funCode: 478
      numArgs: 2
      bytecode: 484241a1484141a21841944941141f0045b341dc109e696e76616c6964206272616e636820696e666c6174696f6e20626f6e7573494149421f0045dd45cb01109e696e76616c696420636861696e20696e666c6174696f6e20616d6f756e74
      source: >
         or(selfIsConsumedOutput,and(selfIsProducedOutput,if(isBranchTransaction,require(equal(uint8Bytes($0),branchInflationBonusFromRandomnessProof(_producedVRFProof)),!!!invalid_branch_inflation_bonus),require(lessOrEqualThan(uint8Bytes($0),_calcChainInflationAmountForPredecessor(selfChainPredecessorInputIndex($1))),!!!invalid_chain_inflation_amount)),))
   -
      sym: "msgED25519"
      funCode: 479
      numArgs: 2
      bytecode: 484241a14c4141a21400444a45ae418a01
      source: >
         or(selfIsConsumedOutput,and(selfIsProducedOutput,equal($0,blake2b(publicKeyED25519(txSignature))),$1))
   -
      sym: "selfReferencedChainData"
      funCode: 480
      numArgs: 0
      bytecode: 4d46458341a98245c98100
      source: >
         parseInlineDataArgument(consumedConstraintByIndex(selfUnlockParameters),#chain,0)
   -
      sym: "selfReferencedChainIDAdjusted"
      funCode: 481
      numArgs: 1
      bytecode: 181900444a45861241a9810000
      source: >
         if(isZero($0),blake2b(inputIDByIndex(byte(selfUnlockParameters,0))),$0)
   -
      sym: "validChainUnlock"
      funCode: 482
      numArgs: 2
      bytecode: 4c41141601880000000000000002140045e11141e08100811f141245840181028100
      source: >
         and(equal(len($1),u64/2),equal($0,selfReferencedChainIDAdjusted(slice(selfReferencedChainData,0,31))),equal(byte(unlockParamsByConstraintIndex($1),2),0))
   -
      sym: "chainLock"
      funCode: 483
      numArgs: 1
      bytecode: 4c4149411441a4810110986c6f636b73206d75737420626520617420626c6f636b203141b848424c4141a24941141600880000000000000020109e33322d62797465206c6f6e6720617267756d656e742065787065637465644941171900109a6e6f6e207a65726f20617267756d656e742065787065637465644c4141a1171441a31241a9810049e20041a9
      source: >
         and(require(equal(selfBlockIndex,1),!!!locks_must_be_at_block_1),selfMustStandardAmount,or(and(selfIsProducedOutput,require(equal(len($0),u64/32),!!!32-byte_long_argument_expected),require(not(isZero($0)),!!!non_zero_argument_expected)),and(selfIsConsumedOutput,not(equal(selfOutputIndex,byte(selfUnlockParameters,0))),validChainUnlock($0,selfUnlockParameters))))
   -
      sym: "c"
      funCode: 484
      numArgs: 1
      bytecode: 45e300
      source: >
         chainLock($0)
   -
      sym: "immutable"
      funCode: 485
      numArgs: 1
      bytecode: 4c424c4141a214444c459c120081008245c9459c120081014c4141a114459c12008101458248401245ab1200810081001241a98100144d46458248401245ab1200810081001241a9810141a0810048401245ab1200810081011241a98100109b696d6d757461626c6520636f6e73747261696e74206661696c6564
      source: >
         or(and(selfIsProducedOutput,equal(parsePrefixBytecode(selfSiblingConstraint(byte($0,0))),#chain),selfSiblingConstraint(byte($0,1))),and(selfIsConsumedOutput,equal(selfSiblingConstraint(byte($0,1)),producedConstraintByIndex(concat(byte(selfSiblingUnlockBlock(byte($0,0)),0),byte(selfUnlockParameters,0)))),equal(parseInlineDataArgument(producedConstraintByIndex(concat(byte(selfSiblingUnlockBlock(byte($0,0)),0),byte(selfUnlockParameters,1))),selfBytecodePrefix,0),concat(byte(selfSiblingUnlockBlock(byte($0,0)),1),byte(selfUnlockParameters,0)))),!!!immutable_constraint_failed)
   -
      sym: "commitToSibling"
      funCode: 486
      numArgs: 2
      bytecode: 4c42484141a117140041a3484141a21401444a45810010a1636f6d6d6974546f5369626c696e6720636f6e73747261696e74206661696c6564
      source: >
         or(and(selfIsConsumedOutput,not(equal($0,selfOutputIndex))),and(selfIsProducedOutput,equal($1,blake2b(producedOutputByIndex($0)))),!!!commitToSibling_constraint_failed)
   -
      sym: "minimumDelegatedAmount"
      funCode: 487
      numArgs: 0
      bytecode: 880000000002faf080
      source: >
         u64/50000000
   -
      sym: "delegationPaceTicks"
      funCode: 488
      numArgs: 0
      bytecode: 880000000000000100
      source: >
         u64/256
   -
      sym: "selfSiblingUnlockParams"
      funCode: 489
      numArgs: 1
      bytecode: 484f458041a300
      source: >
         atTuple8(unlockParamsByIndex(selfOutputIndex),$0)
   -
      sym: "_enforceDelegationTargetConstraintsOnSuccessor"
      funCode: 490
      numArgs: 3
      bytecode: 5041014941494241b645b502109a616d6f756e742073686f756c64206e6f74206465637265617365494114484f02416c459c416c10966c6f636b206d75737420626520696d6d757461626c654941141245e90081028100109e636861696e206d757374206265207374617465207472616e736974696f6e
      source: >
         and($1,require(lessOrEqualThan(selfAmountValue,amountValue($2)),!!!amount_should_not_decrease),require(equal(atTuple8($2,lockConstraintIndex),selfSiblingConstraint(lockConstraintIndex)),!!!lock_must_be_immutable),require(equal(byte(selfSiblingUnlockParams($0),2),0),!!!chain_must_be_state_transition))
   -
      sym: "_openDelegationSlotMap"
      funCode: 491
      numArgs: 0
      bytecode: 86ffffffff0000
      source: >
         0xffffffff0000
   -
      sym: "isOpenDelegationSlot"
      funCode: 492
      numArgs: 2
      bytecode: 17191241eb121e1a110081008103011641eb8107
      source: >
         not(isZero(byte(_openDelegationSlotMap,byte(mod(add(slice($0,0,3),$1),len(_openDelegationSlotMap)),7))))
   -
      sym: "_selfSuccessorChainData"
      funCode: 493
      numArgs: 1
      bytecode: 4d4645821145e900810081018245c98100
      source: >
         parseInlineDataArgument(producedConstraintByIndex(slice(selfSiblingUnlockParams($0),0,1)),#chain,0)
   -
      sym: "_validDelegationChainPace"
      funCode: 494
      numArgs: 1
      bytecode: 48421945c245ca004941494241e8485145cc00418b109b77726f6e672064656c65676174696f6e20636861696e2070616365
      source: >
         or(isZero(chainID(selfChainData($0))),require(lessOrEqualThan(delegationPaceTicks,ticksBefore(selfChainPredecessorTimestamp($0),txTimestampBytes)),!!!wrong_delegation_chain_pace))
   -
      sym: "delegationLock"
      funCode: 495
      numArgs: 5
      bytecode: 5041496d0081014941484114160388000000000000000514160488000000000000000810ab6172677320243320616e64202434206d757374206265203520616e642038206279746573206c656e6774684941174194109f64656c65676174696f6e2073686f756c64206e6f74206265206272616e636848425c4141a2494114444c459c008245c9109c77726f6e6720636861696e20636f6e73747261696e7420696e6465784941494441b641e710a264656c65676174696f6e20616d6f756e742069732062656c6f77206d696e696d756d494117140081ff10a9636861696e20636f6e73747261696e7420696e6465782030786666206973206e6f7420616c6f77656445ee000102484141a14842024841494149ec45ed00418e10996d757374206265206f6e206c697175696469747920736c6f7449414dea000145811245e900810010a177726f6e672064656c65676174696f6e2074617267657420737563636573736f72
      source: >
         and(mustSize($0,1),require(and(equal(len($3),u64/5),equal(len($4),u64/8)),!!!args_$3_and_$4_must_be_5_and_8_bytes_length),require(not(isBranchTransaction),!!!delegation_should_not_be_branch),or(and(selfIsProducedOutput,require(equal(parsePrefixBytecode(selfSiblingConstraint($0)),#chain),!!!wrong_chain_constraint_index),require(greaterOrEqualThan(selfAmountValue,minimumDelegatedAmount),!!!delegation_amount_is_below_minimum),require(not(equal($0,0xff)),!!!chain_constraint_index_0xff_is_not_alowed),_validDelegationChainPace($0),$1,$2),and(selfIsConsumedOutput,or($2,and(require(isOpenDelegationSlot(_selfSuccessorChainData($0),txTimeSlot),!!!must_be_on_liquidity_slot),require(_enforceDelegationTargetConstraintsOnSuccessor($0,$1,producedOutputByIndex(byte(selfSiblingUnlockParams($0),0))),!!!wrong_delegation_target_successor))))))
   -
      sym: "total"
      funCode: 496
      numArgs: 1
      bytecode: 4941484241a11400418d109e746f74616c20616d6f756e7420636f6e73747261696e74206661696c6564
      source: >
         require(or(selfIsConsumedOutput,equal($0,txTotalProducedAmount),),!!!total_amount_constraint_failed)
# END EXTENDED function definitions (defined by EasyFL formulas)
# END all function definitions
```