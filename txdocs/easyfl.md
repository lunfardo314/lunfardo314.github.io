
# EasyFL: a simple functional language

## Introduction
**EasyFL** stands for **Easy** **F**unctional **L**anguage. It is a very simple, a LISP-like functional programming language, without recursion and `eval` function though. It is extendable and is based on platform-independent bytecode.

The *EasyFL* compiler, a core library and runtime engine are available at the [EasyFL repository](https://github.com/lunfardo314/easyfl). _EasyFL_ is the scripting language used in the Proxima UTXO transactions.  

The requirements for such a transaction model extension are:
* minimalism and maximum simplicity of the language and of the runtime semantics
* easy formally verifiable, and, potentially, efficiently zk-provable
* as tiny bytecode as possible
* determinism of the compiler and of interpretation
* source easily readable by humans
* minimal set of hardcoded primitives (_op-codes_)
* extendable with higher level concepts by the means of the language itself 
* extendable standard library
* bounded nature of the computational model, no need for gas budgeting, non-Turing complete verification-oriented, etc. This is closely related to simplicity and other the requirements above.

The models such as *Bitcoin Script*, *Algorand VM* and the likes meet most of the requirements, exept verifiability, understandability and minimalism. To make language understandable, verifiable and minimalistic we choose path of the pure functional style of it.

## Characteristics of *EasyFL*

The following are traits of the *EasyFL*.
* it is minimalist and very simple. It minimizes chances for all kind of implementation bugs. There is not much more to learn  beyond this preliminary presentation
* it is a **pure functional language**. The constraint script semantics is a function call which returns *yes/no* or panics. Only *yes* indicates satisfied constraint. Other outcomes invalidates the transaction. Each function call has no side effects. Functional semantics is an advantage over VM/sequential processor-based scripting, such as *Bitcoin Script* or *Algorand VM*.
* the embeddable transaction constraint takes a form of the *EasyFL* expression, such as `lessThan(selfAmount, 1000)`
* the computational model of *EasyFL* is **stateless** and **non-Turing-equivalent** by intention. This makes no need for gas budgeting, however it does not prevent introduction of gas burn for other purposes. Note, that wrt computational model, all of them, *EasyFL*, *Bitcoin Script* and *Algorand VM* (the *stateless TEAL*), are non-Turing complete and therefore **all are fundamentally equivalent to the finite state automaton**.
* the **runtime library** is a runtime environment of the *EasyFL*. The library of functions is extendable by embedding (a) hardcoded function hooks, for example for complex cryptographic computations or (b) by *EasyFL* expressions
* the above makes each transaction a finite **circuit**:
    * it is bounded by nature, so, ideal for validation of bounded data structures, such as UTXO transactions
    * it is **formally verifiable**. Theoretically it is possible to automatically *prove* validity statements about the data structure form the set of constraint. For example. "the output cannot be consumed without knowing a private key or a validity proof". The *EasyFL* constraint is a programm and same time its specification.
    * it **zk-friendly** without the need of recursive zk-techniques such as PLONK. (this potentially can make UTXO ledger based on *EasyFL* constraints, zk-provable. It is a trait which may be explored in the future)
* *EasyFL* is a simplistic low level language, operating at the byte level, i.e. before any serialization logic. The level of the language can be increased by the means provided in the language itself.
* the *EasyFl* program exists in the form of **source code**, **canonical bytecode** and evaluation tree form.
    * the *source code* is human readable
    * the *canonical bytecode* is deterministically compiled from the *source code*
    * the *canonical bytecode* is highly compressed. This makes it ideal for embedding inline into the constraint into any restricted environments, including UTXO transactions
    * the internal, platform specific, evaluation tree is deterministically generated from the canonical bytecode
* the execution means an evaluation of the *EasyFL* expression in the context of *EasyFL library* environment and the externally provided data, namely the data structure being validated

Example: the following expression states that the length of the unlock block for the consumed output must be 96 bytes long:

```Go!
equal(len8(selfUnlockBlock), 96)
```

In the above we assume the following:
* expression is evaluated for the particular consumed UTXO
* function `selfUnlockBlock` returns the bytes of the unlock block corresponding to the consumed UTXO. If it does not exist, the evaluation panics.

## The language

### Data types
The only data type in *EasyFL* is *byte array* aka *byte slice*. It can be empty.

Function calls take *byte arrays* as call arguments and returns a *byte array* as a result.

The empty byte array is interpreted as `false` value wherever appropriate. Any non-empty value is interpreted as `true`.

The source language provides shortcuts, such as `u32/1337` means 4 bytes of *big-endian* bytes of `uint32(1337)`.

### Expressions
*EastFL source* is any ASCII text with line delimiters.

Any text in the line from symbols `//` to the end of line are comments. They have no effect on the execution.

*Expression* is a text where all *space* symbols (`\n`, `\r`, `\t`, ` `) are ignored. The source code of the `expression `is parsed to a sequence of `lexems`. A `lexem` is an ASCII string between `delimiters`.

The `delimiters` are `(`, `)` and `,`


Source of the `expression` has the following form of the function `call`:

`<expression> ::= <funName>[(<call args>)] || <constant literal>`

Here with meta symbols `[]` we enclose optional part.

`<funName>` is a name of the function which is present in the library or is a `constant literal`.
`Constant literals` are distinguished from library function names by syntax (see below).

Each function in the library defines its *arity*, the number of parameters it takes.

Each function can have `arity` from 0 to 15, i.e. the function can take from none to 15 call arguments. Also, an embedded library function can define it takes any number from 0 to 15 of call arguments, i.e. to be a *vararg* function.

If function `fun` takes 0 arguments, the expressions `fun` and `fun()` are equivalent. For example `selfUnlockParameters` is a function call with no arguments, however it returns a value, a byte array, upon evaluation.

`<call args>` is a comma-delimited list of `<expression>`-s. The list can be empty.

### Constant literals
Each `constant literal` represents an expression:
* decimal number between `0` and `255`, it is a 1-byte array with the respective value. For example `0`, `42` are correct `constant literals` while `1337` is not.
* a literal with the prefix `0x` is interpreted as a hexadecimal representation of the `byte array` of length, less than 127 bytes. For example `0xff0102` is a 3-byte array, while `0x123` is incorrect
* in the literal with the prefix `u16/` the tail after the prefix is interpreted as 2-byte array, a *big-endian* representation of `uint16`
* in the literal with the prefix `u32/` the tail after the prefix is interpreted as 4-byte array, a *big-endian* representation of `uint32`
* in the literal with the prefix `u64/` the tail after the prefix is interpreted as 8-byte array, a *big-endian* representation of `uint64`
* the literal which starts with `!!!` is a a call to embedded `fail` function. The tail after the `!!!` prefix is interpreted as inline error message in the `panic` statement. For example, when and if expression `!!!not_enough_storage_deposit` is evaluated, it results to the whole scipt failed with the message `not enough storage deposit` (the `_` are replaced with spaces)
* the literal which starts with `x/` represents inline *EasyFL* formula in its canonic bytecode form, presented as hexadecimal. For example literal expression `x/10856369616f21` is equivalent to the literal `!!!ciao!`

(Note. Options for `constant literals` may be extended in the future, for example *little-endian* numbers, signed integers, big-ints with various encodings etc)

### Examples 1

The standard library contains embedded functions. Here are some of them: `fail`, `concat`, `slice`, `byte`, `equal`, `if`, `and`, `or`, `not`, `len8` and many others. The following are valid expressions:

* `slice(0x0102,0,0)` takes the element with index 0 (slice bounds are inclusive), return 1-byte long array.
* `byte(0x0102, 0)` is an equivalent to the above
* `concat(1, 5)` is equivalent to `0x0105` and is equivalent to `u16/21`
* `concat` always returns empty slice
* `equal(concat(1, 5), 0x01ff)` always returns empty slice, i.e. `false`
* `if(0, u16/31415, u32/271828` will always evaluate to 2-byte slice `u16/31415`
* `or` will always return empty slice `false`
* `and` will always return non-empty slice `true`, undefined which one exactly

### Evaluation
Expressions are evaluated in the form of the internal evaluation tree, derived from the bytecode. So, the workflow is always like this:

`<expression source> -> <canonical bytecode> -> <evaluation tree> -> <evaluation>`.

The engine (function `EvalExpression`) is using **lazy evaluation**. It means argument expression is only evaluated when and if it is needed for the evaluation of the context where it is used as a parameter. For example, the expression:
`if(concat, byte(0,1), 0x01)` will never panic even if `byte(0,1)` always panics (see *Exceptions* below). It is because `concat` always returns `false` and `if` function always evaluates only one of two branches.


### Exceptions
Evaluation of the expression may fail with the panic. For example, expression `byte(0,1)` will always panic, because it tries to take a byte with index `1` from the 1-byte array `[0]`.

The embedded function `fail` always panics with its only argument interpreted as the error message/string. The `!!!<msg>` is a shortcut literal of the `fail` function call.

The evaluation engine (the Go function `EvalFromBinary`) does not process exceptions. The transaction validation context, which invokes the evaluation engine, must intercept panic and treat transaction as invalid.

### Parameters of the expression
An `expression` can use special function calls `$0`, `$1` ... `$15`.  They represent *parameters of the expression*. Parameters of the expression will be instantiated with values whenever `expression` is evaluated and it call the corresponding `$i` function. The use of the parameter `$i` in the expression means that at least `i+1` arguments must be supplied when `expression` is evaluated.

For example expression `or($3)` will return 4th argument, however all 4 must be supplied, only first 3 won't be used.

Expression parameters can be used at any level of the expression, i.e. `not(not(not(not($0))))` is a correct expression, it will require 1 argument.

### Examples 2
* `if($0,$2,$1)` will evaluate `$2` if `$0` will return true and will evaluate `$1` if `$0` is nil. It deserves the name `ifNot`.
* `concat($0, $0, $0, $0)` will repeat argument by concatenating it 4 times.

In Go, the expressions can be evaluated the following way:

```go
ret, err := easyfl.EvalFromSource(nil, "concat($1,$0)", []byte{222}, []byte{111})
```
will compile the source to the bytecode form, will evaluate it with provided arguments and will return reversed slice:
```go
[]byte{111,222}
```

### Extension of the library
The semantics of execution of the expressions depends on the functions itself. The runtime environment of *EasyFL* assumes `the library`, which contains all function definitions, available for the evaluation engine. For the UTXO transaction validation, the library must be the same on each node.

There are two types of functions: `embedded` and `extended`.

#### Embedded functions
`Embedded` functions are hardcoded executable code of the host environment, for example Go code. They are defined by `name`, `arity` and the Go function to be executed (or other language environment). Example of embedding:

Function with variable number of arguments.
```go
EmbedShort("concat", -1, func (par *CallParams) []byte {
	var buf bytes.Buffer
	for i := byte(0); i < par.Arity(); i++ {
		buf.Write(par.Arg(i))
	}
	return buf.Bytes()
})
```

Function with fixed `arity` 3.
```go
EmbedLong("validSignatureED25519", 3, func(ctx *CallParams) []byte {
	msg := ctx.Arg(0)
	signature := ctx.Arg(1)
	pubKey := ctx.Arg(2)
	if ed25519.Verify(pubKey, msg, signature) {
		return []byte{0xff} // anything not nil is true
	}
	return nil
})
```

Embedded functions usually have a very simple and clear semantics. They usually contains very core functions or very complicated, such as cryptography.

The embedded code accesses arguments of the call through provided context of type `ctx *CallParams`. The global data structure being validated, such as UTXO transaction, is accessed as `ctx.DataContext()`. This way embedded code have access to the whole data context it is validating.

Notably, the embedded code is running any code on the host environment, so it is not restricted to the *non-Turing equivalence*, i.e. it may run any loops and queries on the provided data context. This is up to the developer of the embedded code with all the consequences, because embedded code is out of control of the transaction validation context.

Note, that embedded code is always provided by the node developer. Meanwhile, the transaction production environment can only provide *EasyFL* expessions, bytecode or source and they are protected by the bounded nature of the computation model (see *Extended functions* below).

So, the embedded functions can also contain calls to other, more complicated, environmens, VMs and interpreters, such as EVM or Wasm. **Function embedding is a natural point where ledger protocol may be extended.**

The call context `ctx *CallParams` provides access to parameters of the call and access to the data structure the expression is validating. In the UTXO case the data structure is the UTXO transaction itself.

#### Extended functions

Extended funtions are defined by expression in the source form. For example:

```go
	Extend("nil", "or")
	Extend("false", "or")
	Extend("true", "and")
	Extend("lessOrEqualThan", "or(lessThan($0,$1),equal($0,$1))")	
```
adds functions `nil` (0 parameters, call `or()` always returns `false/nil` and `and` always returns some non-empty slice, interpreted as `true` ) and `lessOrEqualThan` (2 parameters) as an expressions to the library. The `Extend` call compiles expression and prepares it for evaluation. It automatically calculates `arity` of the function as `i+1`, where `$i` is the largest number of the parameter.

The strict requirement is: **any function referenced in the expression must already exist in the library**. This restriction makes the *EasyFL* compiler extemely simple and **prevents recursive definitions of functions**. It also and makes the computational model of *EasyFL* expressions **non-Turing equivalent**, just as intended.

#### Extension with many functions
*EasyFL* compiler provides following notation to extend library with many function definition. It is usefull extend library with more complex transaction constraints.

Each library extension of this kind has a form:

`func <function name>: <expression>`

In the source may be many these function definitions.

#### Local libraries
The *EasyFL* compiled and runtime support embedable libraries, so called **local libraries**. The *local library* is a collection of *EasyFL* functions compiled into the canonical bytecode format. Another  *EasyFL* function can call (invoke) an *EasyFL* function from the compiled local library, which is provided as parameter. This feature enables use cases, for example when constraint requires to know another unocking script to unlock the first one. Example may be hash-locking the output and to unlock it we must provide script as pre-image of the hash.

## Bigger example: ED25519 sig lock constraint
The following is an example of a *sigLocED25519* constraint, which only allows transaction to be valid, if the output is unlocked by the valid ED25519 signature of the transaction essence or points to another input, which contains a valid signature verifiable with  the same address.

The source code is taken from the `EasyUTXO` PoC ledger implementation. It is provided here to demonstrate expressiveness of the language.

```go
// ED25519 address constraint wraps 32 bytes address, the blake2b hash of the public key
// For example expression 'addressED25519(0x010203040506..)' used as constraint in the output makes 
// the output unlockable only with the presence of signature correspomding 
// to the address '0x010203040506..'

// $0 = address data 32 bytes
// $1 = signature
// $2 = public key
// return true if transaction essence signature is valid for the address
func unlockedWithSigED25519: and(
	equal($0, blake2b($2)), 		       // address in the address data must be equal to the hash of the public key
	validSignatureED25519(txEssenceBytes, $1, $2)
)

// 'unlockedByReference'' specifies validation of the input unlock with the reference.
// The referenced constraint must be exactly the same  but with strictly lesser index.
// This prevents from cycles and forces some other unlock mechanism up in the list of outputs
func unlockedByReference: and(
	lessThan(selfUnlockParameters, selfOutputIndex),              // unlock parameter must point to another input with 
							                                      // strictly smaller index. This prevents reference cycles	
	equal(self, consumedLockByOutputIndex(selfUnlockParameters))  // the referenced constraint bytes must be equal to the self constraint bytes
)

// if it is 'produced' invocation context (constraint invoked in the input), only size of the address is checked
// Otherwise the first will check first condition if it is unlocked by reference, otherwise checks unlocking signature
// Second condition not evaluated if the first is true
// $0 - ED25519 address, 32 byte blake2b hash of the public key
func addressED25519: and(
	equal(selfBlockIndex,2), // locks must be at block #2
	or(
		and(
			selfIsProducedOutput, 
			equal(len8($0), 32) 
		),
		and(
			selfIsConsumedOutput, 
			or(
					// if it is unlocked with reference, the signature is not checked
				unlockedByReference,
					// tx signature is checked
				unlockedWithSigED25519($0, signatureED25519(txSignature), publicKeyED25519(txSignature)) 
			)
		),
		!!!addressED25519_unlock_failed
	)
)
```

## Extension of Stardust UTXO ledger with *EasyFL* constraints

This a draft plan how *EasyFL* could be made a part of the Stardust specs. It will require adding one new feature block. It means full backwards compatibility. This would make existing Stadust ledger programmable with huge variety of use cases: from NFT logic to DeFi.

The special *EasyFL* feature block will contain a compiled *EasyFL* bytecode of the constraint. In many situations it will be a handfull of bytes long.

The validation of this feature block will mean evaluating the encoded expression in the context of the transaction (global data) and the invocation location:
* is it a consumed output, or produced output of the transaction, the `yes/no` flag
* the output index (currently 1 byte is enough). It is either input index, or output index
* the index of the invoked *EasyFL* feature block in the output
  The all 3 things above may be compressed in one `invocation path/location` concept. It will be 3 byte-long value.

We need to extend *EasyFL* library by embedding functions, which provide the script access to the elements of the transaction. The access should be parametrized by the invocation path values:
* access to the data of the corresponding `unlockBlock`
* access to the data of any specified block of any input/output, like `blockData(consumedYN, outputIndex, blockIndex)`.

The current high level concept of the unlock block in Stardust should be extended with the possibility to append any raw binary data to it. It will not be interpreted by the `iota.go` validation logic, but `EasyFL` script will access it by a special embedded function.

These simple extentions of the current Stardust will enormously increase the flexibility and extendability of the Stardust ledger. Sky will be the limit.

Of course, it will require special functions for the ZK-validation, BLS signature validation and all other advanced cryptography

### Example

Let's imagine we have the following embedded functions:

* function `@` always returns 3-byte array:
    *  0-byte contains `0` if the invoked script is in the consumed output, `1` if it is in the produced output
    *  1-byte contains index of the output in the transaction
    *  2-byte contains block index of the invoked constraint
*  function `unlockData(idx)` return bytes attached to the unlock block with the index `idx` (1 byte)
*  function `amountOut(idx)` returns the amount of base tokens of the produced output with index `idx`
*  functions `addressIn(idx)` and `addressOut(idx)` are addresses of the corresponding consumed output and produced output.

So, the expression `unlockData(byte(@,1))` returns unlock block data of the consumed output, and expression `addressOut(byte(unlockData(byte(@,1)),0))` is the address of produced output, index of which is provided in the 0-byte of the unlock data.

Then the following expression is a return condition: the consumer of the output must insert output which sends at least 10000 base tokens to the sender:
```go
if(
	equal(byte(@,0),0),  // it is a consumed output
	and(
		greaterOrEqualThan(
			amountOut(byte(unlockData(byte(@,1)),0)), 
			u64/10000
		),
		equal(
			addressIn(byte(@,1)),
			addressOut(byte(unlockData(byte(@,1)),0))
		)
	),
	and      // always true (no effect) for a produced output
)
```

More preceisely, it expresses the following constraint:

to consume the output with this constraint:
- you have to provide index of a produced output in the unlock data of the input, in the byte at index 0
- **and** the referenced produced output must contain address equal to the address of the consumed output
- **and** the amount of base tokens in the referenced produced output must be more than 10000

Estimated size of the binary for this constraint should be some 15-20 bytes (never really compiled, sorry).