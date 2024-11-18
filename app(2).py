from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import mysql.connector

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_C1', methods=['POST'])
def add_C1():
    if request.method == 'POST':
        try:
            
            option_list.append(1)
            return jsonify({'message': 'Element added to the list!'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
