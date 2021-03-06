import functools
from urllib import parse

from flask import (
    Blueprint, session, g, request, render_template, redirect,
    url_for, flash
)
from flask_socketio import (
    join_room, leave_room, emit, send
)
import flask_socketio as socketio

from chatroom import config
from chatroom import utils
from chatroom.auth import login_required
from chatroom.database import *
from chatroom import socket

# to check if logged in, you should do it in http endpoint.
@socket.on('join', namespace='/chat')
def join(data):
    userId=session.get('userId')
    userName=session.get('userName')
    userColorName=session.get('userColorName')
    roomId=session.get('roomId')

    join_room(roomId)
    emit('status', {
        'userId':               userId,
        'userName':             userName,
        'userColorCode':        config.COLOR[userColorName],
        'messageContent':       "Entered room."
    }, room=roomId)

@socket.on('submit', namespace='/chat')
def submit(data):
    if data['content']=='':
        return

    userId=session.get('userId')
    userName=session.get('userName')
    userColorName=session.get('userColorName')
    roomId=session.get('roomId')

    msg=Message({
        'messageId':        utils.get_message_id(),
        'userId':           userId,
        'roomId':           roomId,
        'messageTimeStamp': utils.get_time(),
        'messageContent':   parse.unquote(data['content'])
    })
    msg_db=MsgDatabase()
    msg_db.insert(msg)
    emit('listen', {
        'messageId':        msg['messageId'],
        'userId':           msg['userId'],
        'userName':         userName,
        'userColorCode':    config.COLOR[userColorName],
        'roomId':           msg['roomId'],
        'messageTimeStamp': msg['messageTimeStamp'],
        'messageContent':   msg['messageContent']
    }, room=msg['roomId'])

@socket.on('leave', namespace='/chat')
def leave(data):
    print("Leave")
    userId=session.get('userId')
    userName=session.get('userName')
    roomId=session.get('roomId')

    leave_room(roomId)
    emit('status', {
        'userId':               userId,
        'userName':             userName,
        'content':              "Left room."
    }, room=roomId)
    socketio.disconnect()
