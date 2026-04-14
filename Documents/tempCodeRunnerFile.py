from flask import Flask, render_template, redirect, request, session, url_for
import mysql.connector
from config import DB_CONFIG