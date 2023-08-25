#!/usr/bin/env python3
"""
    A card game
"""

import sys
import os
import random
import tkinter as tk
from typing import Union, Tuple
from tkinter import ttk
from tkinter import (N, S, E, W, PhotoImage)
from tools import interpret_file
from lprint import print_debug, print_error, red, blue, yellow

CARD_IMAGES = list()
PLACEHOLDER_CARD = "cards/card.png"
class Card:
    """
        A class to contain Cards
    """
    def __init__(self, root, name="card", imagepath=PLACEHOLDER_CARD, *, command=None, gameaction=None):
        self.root = root
        self.name = name
        self.imagepath = imagepath
        if not os.path.exists(imagepath):
            print_error(f"{imagepath} doesn't exists")
            sys.exit()

        self.image = None
        self.command = command
        self.gameaction = gameaction
    def create(self):
        """
            Create a image label card
        """
        self.image = PhotoImage(file=self.imagepath)
        CARD_IMAGES.append(self.image)
        label = None
        if not self.command:
            label = ttk.Label(self.root, image=self.image)
        else:
            label = ttk.Label(self.root, image=self.image)
            button_name, function = self.command
            label.bind(button_name, function)
        return label
    def pack(self):
        """ Not implemented """
        print(str(self.pack) + "Not implemented")

class CardContainer:
    """
        A class to contain Card objects
    """
    def __init__(self):
        self.container = list()
        self.names = list()
    def add(self, card: Card):
        """ Add new card """
        self.container.append(card)
        self.names.append(card.name)
    def get_by_name(self, name):
        """ Get card by name """
        for card in self.container:
            if card.name == name:
                return card
        return "No Card" # Return an error in the future
    def get_by_imagepath(self, imagepath):
        """ Get card by imagepath """
        for card in self.container:
            if card.imagepath == imagepath:
                return card
        return "No Card" # Return an error in the future
    def get_random(self):
        name = random.choice(self.names)
        return self.get_by_name(name)


class CardHand:
    """ CardHolder with removability """
    def __init__(self):
        pass




class App:
    """
        Container for the tkinter app
    """
    def __init__(self):
        self.card_container = CardContainer()
        self.width = 1500
        self.height = 750
        window = tk.Tk()
        window.title("Tales of Cards")
        window.geometry(f"{self.width}x{self.height}")
        style = ttk.Style()
        style.configure("TFrame", background="black")
        # window.columnconfigure(0, weight=1)
        window.bind("<Escape>", lambda *args: sys.exit())
        self.root = ttk.Frame(window, style="TFrame")
        self.root.pack(expand=True, fill=tk.BOTH)
        self.root.columnconfigure(0, weight=1)# weight=1)
        self.root.rowconfigure(0)# weight=1)
        self.root.rowconfigure(1)# weight=1)
        self.root.rowconfigure(2)# weight=1)
        # self.root.grid(column=0, row=0, sticky=(N,E,W,S))
        # self.root.columnconfigure(0, weight=1)

        self.frame_pack_self = None
        self.frame_pack_board = None
        self.frame_pack_enemy = None

        self.frame_pack_gameinfo = None
        self.frame_pack_pullcard = None

        self.photoimage_objects = list()
        self.initilaze_game()
        window.mainloop()
    def card_label(self, frame, imagepath=PLACEHOLDER_CARD, *, command=None):
        """
            frame: ttk.Frame = root frame of label
            imagepath: str = image path in string
            command: (str, function) = button name and function
        """
        card_label = Card(frame, imagepath, imagepath, command=command)
        self.card_container.add(card_label)
        label = card_label.create()
        label.name = card_label.name


        return label
    def initilaze_game(self):
        """
            Initilaze the game:
                initilaze_styles: Creates styles so frames are colored
                initilaze_enemy: Creates and initilazes the enemy frame
                initilaze_board: Creates and initilazes the board frame
                initilaze_self: Creates and initilazes the player frame
        """
        self.initilaze_styles()
        self.initilaze_enemy()
        self.initilaze_board()
        self.initilaze_self()
    def initilaze_styles(self):
        """
            Initilaze the styles so frames are colored:
                enemy: Red
                board: Blue
                player(self): Green
        """
        style = ttk.Style()
        style.configure("TFrame")
        style.configure("FrameEnemy.TFrame", background="red")
        style.configure("FrameBoard.TFrame", background="blue")
        style.configure("FrameSelf.TFrame", background="green")
    def initilaze_enemy(self):
        """
            Create the frame for the enemy(frame_enemy) with a height of 1/3. and full width
            Make another frame inside the frame and pack it so cards are centered.
            Create a card_label for test(should remove)
            Add frame_enemy to the grid
        """
        frame_enemy = ttk.Frame(
            self.root,
            style="FrameEnemy.TFrame",
            height=self.height//3,
            width=self.width
                )
        other = ttk.Frame(frame_enemy)
        other.pack()
        self.card_label(other).pack(side=tk.LEFT)
        frame_enemy.grid(column=0, row=0, sticky=(N, S, E, W))
    def initilaze_board(self):
        """
            Create the frame for the board(frame_enemy) with a height of 1/3. and full width
            Create other frame and set it to the self.board_frame_other to reach it from outside
        """
        frame_board = ttk.Frame(self.root, style="FrameBoard.TFrame",
                                height=self.height//3,
                                width=self.width)
        other = ttk.Frame(frame_board, style="FrameBoard.TFrame")
        self.frame_pack_gameinfo = ttk.Frame(frame_board, style="FrameEnemy.TFrame")
        self.frame_pack_pullcard = ttk.Frame(frame_board, style="FrameSelf.TFrame")
        self.frame_pack_gameinfo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.initilaze_gameinfo()
        self.board_frame_other = other
        other.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frame_pack_pullcard.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.initilaze_pullcard()
        self.board_card = self.card_label(other)
        self.board_card.pack()
        frame_board.grid(column=0, row=1, sticky=(N, S, E, W))
    def initilaze_gameinfo(self):
        frame = self.frame_pack_gameinfo
        card = self.card_label(frame)
        card.pack()
    def initilaze_pullcard(self):
        frame = self.frame_pack_pullcard
        card = self.card_label(frame)
        self.pack_to_self(self.card_container.get_random())
        card.pack()
    def get_hand_from_file(self, filename):
        interpreter = interpret_file(filename)
        return interpreter.global_variables["Cards"]
    def prepare_hand(self):
        hand = self.get_hand_from_file("try.toc")
        print_debug(hand)
        for card in hand:
            new_card = hand[card]
            card_name = new_card["name"]
            card_image = new_card["image"]
            card_command = new_card.get("command", None)
            card = (card_name, card_image, card_command)
            self.pack_to_self(card)
    def pack_to_self(self, card: Union[Tuple[str, str, str], Card]):
        """card_label(frame,
                      imagepath="card.png", *,
                      command=None)"""
        frame = self.frame_pack_self
        name = None
        imagepath = None
        command = None
        if type(card) == Card:
            name = card.name
            imagepath = card.imagepath
            command = card.command
        else:
            name = card[0]
            imagepath = card[1]
            command = card[2]
        def commandl(*args):
            if command: command()
            self.frame_self_card_click_event(*args)
        mycommand = ("<Button-1>", commandl)
        card_object = Card(frame, name, imagepath)
        card_label = self.card_label(frame, imagepath, command=mycommand)
        card_label.name = name
        card_label.imagepath = imagepath
        self.card_container.add(card_label)
        print_debug(f"{frame=}, {imagepath=}, {command=}")
        card_label.pack(side=tk.LEFT)


    def initilaze_self(self):
        """
            Create the frame for the board(frame_enemy) with a height of 1/3. and full width
        """
        frame_self = ttk.Frame(self.root, style="FrameSelf.TFrame",
                               height=self.height//3,
                               width=self.width)
        other = ttk.Frame(frame_self)
        self.frame_pack_self = other
        other.pack()
        self.prepare_hand()
#        frame_self.bind("<Button-1>",
#                        lambda *args: self.card_label(other, "card2.png").pack(side=tk.LEFT))
#
#        command = ("<Button-1>", self.frame_self_card_click_event)
#        self.card_label(other, "card.png", command=command).pack(side=tk.LEFT)
#        self.card_label(other, "card2.png", command=command).pack(side=tk.LEFT)
        frame_self.grid(column=0, row=2, sticky=(N, S, E, W))
    def frame_self_card_click_event(self, *args):
        """
            A function to remove the card from hand and
            create the same and add it to the board
        """
        event = args[0]
        self.pack_to_board(event.widget)
        event.widget.destroy()
    def pack_to_board(self, card):
        """
            Destroy board_card
            Create a new Card object
            Pack it to the board_frame_other
        """
        self.board_card.destroy()
        old = self.card_container.get_by_name(card.name)
        cardobject = Card(self.board_frame_other, old.name, old.imagepath)
        self.board_card = cardobject.create()
        self.board_card.pack()
        self.board_card.pack()




app = App()
