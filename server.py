from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

app = Flask(__name__)
app.secret_key = "dev"