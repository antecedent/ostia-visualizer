# ostia-visualizer
Records the construction of a finite-state transducer as done by OSTIA (Onward Subsequential Transducer Inference Algorithm), then plays it back using vis.js.

## Recording

To make use of ostia-visualizer, you will need to run OSTIA on your dataset of choice and obtain a **log**. Alternatively, a sample log is available for demonstration purposes: if this is of interest to you, please proceed to [Playback](#Playback).

* Install [SigmaPie](https://github.com/alenaks/SigmaPie).
* Override its `FST` class with the one provided in the [patch that is found in this repository](https://github.com/antecedent/ostia-visualizer/blob/master/patch/fst_object.py).
* Proceed to invoke OSTIA as usual, which will provide a `FST` object as a return value. Let `fst` be this object.
* `fst.notifications` is now a line-by-line `list` representation of the log. Therefore, you will most likely want to do this:

```python
with open('ostia-log.py', 'w') as ostia_log:
    ostia_log.write('\n'.join(fst.notifications))
```

The log is also a Python script that reenacts the FST construction, hence the .py extension.

## Playback

* Navigate [to this copy of ostia-visualizer](https://antecedent.github.io/ostia-visualizer/) or use your own.
* "Upload" the `ostia-log.py` file or any other one that contains the log.
  * No uploading actually takes place, only client-side computations are involved.
* Interpret the animation that ensues.
