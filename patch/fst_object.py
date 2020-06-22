#!/bin/python3

"""
   A class defining the Finite State Transducer.
   Copyright (C) 2019  Alena Aksenova
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from copy import deepcopy

class NotifyingView():
    
    def __init__(self, inner, identifier, notifications):
        self.inner = inner
        self.identifier = identifier
        self.notifications = notifications
    
    def __len__(self):
        return len(self.inner)

    def __getitem__(self, key):
        item = self.inner[key]
        if type(item) == list:
            return NotifyingView(item, f'{self.identifier}[{self.identifier}.index({repr(item)})]', self.notifications)
        return item

    def __setitem__(self, key, value):
        self.notifications.append(f'{self.identifier}[{repr(key)}] = {repr(value)}')
        self.inner[key] = value

    def __delitem__(self, key):
        self.notifications.append(f'del {self.identifier}[{repr(key)}]')
        del self.inner[key]

    def __iter__(self):
        return iter(NotifyingView(i, f'{self.identifier}[{self.identifier}.index({repr(i)})]', self.notifications) if type(i) == list else i for i in self.inner)
    
    def append(self, value):
        self.notifications.append(f'{self.identifier}.append({repr(value)})')
        self.inner.append(value)
        
    def remove(self, value):
        self.notifications.append(f'{self.identifier}.remove({repr(value)})')
        self.inner.remove(value)


class FST():
    """
    A class representing finite state transducers.
    Attributes:
        Q (list): a list of states;
        Sigma (list): a list of symbols of the input alphabet;
        Gamma (list): a list of symbols of the output alphabet;
        qe (str): name of the unique initial state;
        E (list): a list of transitions;
        stout (dict): a collection of state outputs.
    """
    def __init__(self, Sigma=None, Gamma=None):
        """ Initializes the FST object. """
        self.copy_counter = [0]
        self.identifier = f'FSTs[{self.copy_counter[0]}]'
        self.notifications = []
        self._Q = NotifyingView([], self.identifier + '.Q', self.notifications)
        self._E = NotifyingView([], self.identifier + '.E', self.notifications)
        self.Sigma = Sigma
        self.Gamma = Gamma
        self.qe = ""
        self._stout = NotifyingView({}, self.identifier + '.stout', self.notifications)
        
    def __del__(self):
        self.notifications.append(f'del {self.identifier}')
    
    @property
    def Q(self):
        return self._Q
    
    @property
    def E(self):
        return self._E

    @property
    def stout(self):
        return self._stout

    @Q.setter
    def Q(self, value):
        old_value = self._Q
        self._Q = NotifyingView(value, self.identifier + '.Q', self.notifications)
        for deletion in set(old_value) - set(value):
            self.notifications.append(f'{self.identifier}.Q.remove({repr(deletion)})')
        for addition in set(value) - set(old_value):
            self.notifications.append(f'{self.identifier}.Q.append({repr(addition)})')
        
    @E.setter
    def E(self, value):
        old_value = self._E
        self._E = NotifyingView(value, self.identifier + '.E', self.notifications)
        for deletion in set(tuple(e) for e in old_value) - set(tuple(e) for e in value):
            self.notifications.append(f'{self.identifier}.E.remove({repr(list(deletion))})')
        for addition in set(tuple(e) for e in value) - set(tuple(e) for e in old_value):
            self.notifications.append(f'{self.identifier}.E.append({repr(list(addition))})')

    @stout.setter
    def stout(self, value):
        old_value = self._stout
        self._stout = NotifyingView(value, self.identifier + '.stout', self.notifications)
        for deletion in set(old_value) - set(value):
            self.notifications.append(f'del {self.identifier}.stout[{repr(deletion)}]')
        for addition in set(value) - set(old_value):
            self.notifications.append(f'{self.identifier}.stout[{repr(addition)}] = {repr(value[addition])}')

    def color_state(self, q, color):
        self.notifications.append(f'color_state({repr(q)}, {repr(color)})')

    def rewrite(self, w):
        """
        Rewrites the given string with respect to the rules represented
        in the current FST.
        Arguments:
            w (str): a string that needs to be rewritten.
        Outputs:
            str: the translation of the input string.
        """
        if self.Q == None:
            raise ValueError("The transducer needs to be constructed.")
        
        # move through the transducer and write the output
        result = ""
        current_state = ""
        moved = False
        for i in range(len(w)):
            for tr in self.E:
                if tr[0] == current_state and tr[1] == w[i]:
                    result += tr[2]
                    current_state, moved = tr[3], True
                    break
            if moved == False:
                raise ValueError("This string cannot be read by the current transducer.")
                
        # add the final state output
        if self.stout[current_state] != "*":
            result += self.stout[current_state]
            
        return result
        
        
        
    def copy_fst(self):
        """
        Produces a deep copy of the current FST.
        Returns:
            T (FST): a copy of the current FST.
        """
        T = FST()
        T._Q = self._Q
        T._E = self._E
        T.copy_counter = self.copy_counter
        T.copy_counter[0] += 1
        T.identifier = f'FSTs[{self.copy_counter[0]}]'
        T.notifications = self.notifications
        T.notifications.append(f'FSTs[{self.copy_counter[0]}] = {self.identifier}.copy_fst()')
        T.Q = deepcopy(self.Q.inner)
        T.Sigma = deepcopy(self.Sigma)
        T.Gamma = deepcopy(self.Gamma)
        T.E = deepcopy(self.E.inner)
        T.stout = deepcopy(self.stout.inner)
        
        return T
