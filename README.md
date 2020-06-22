# ostia-visualizer
Records the construction of a finite-state transducer as done by OSTIA (Onward Subsequential Transducer Inference Algorithm), then plays it back using vis.js.

## Recording

To make use of ostia-visualizer, you will need to run OSTIA on your dataset of choice and obtain a **log**. 

(Alternatively, a sample log is available for demonstration purposes: if this is of interest to you, please proceed to [Playback](#Playback).)

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

## Tracking state colors

OSTIA colors the transducer's states red and blue. If one desires to reflect that in the visualization, it is also necessary to redefine the `ostia` function as follows:

```python
def ostia(S, Sigma, Gamma):
    """This function implements OSTIA (Onward Subsequential Transduction
    Inference Algorithm).

    Arguments:
        S (list): a list of pairs (o, t), where `o` is the original
            string, and `t` is its translation;
        Sigma (list): the input alphabet;
        Gamma (list): the output alphabet.
    Returns:
        FST: a transducer defining the mapping.
    """
    # create a template of the onward PTT
    T = build_ptt(S, Sigma, Gamma)
    T = onward_ptt(T, "", "")[0]

    # color the nodes
    red = [""]
    blue = [tr[3] for tr in T.E if tr[0] == "" and len(tr[1]) == 1]

    T.color_state("", "red")

    for blue_state in blue:
        T.color_state(blue_state, "blue")

    # choose a blue state
    while len(blue) != 0:
        blue_state = blue[0]

        # if exists state that we can merge with, do it
        exists = False
        for red_state in red:

            # if you already merged that blue state with something, stop
            if exists == True:
                break

            # try to merge these two states
            if ostia_merge(T, red_state, blue_state):
                T = ostia_merge(T, red_state, blue_state)
                exists = True

        # if it is not possible, color that blue state red
        if not exists:
            red.append(blue_state)
            T.color_state(blue_state, "red")

        # if possible, remove the folded state from the list of states
        else:
            T.Q.remove(blue_state)
            del T.stout[blue_state]

        # add in blue list other states accessible from the red ones that are not red
        blue = []
        for tr in T.E:
            if tr[0] in red and tr[3] not in red:
                blue.append(tr[3])
                T.color_state(tr[3], "blue")

    # clean the transducer from non-reachable states
    T = ostia_clean(T)
    T.E = [tuple(i) for i in T.E]

    return T

```
