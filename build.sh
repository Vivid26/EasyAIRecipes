#!/usr/bin/env bash
cd client
npm install
npm run build
cd ..
pip install -r server/requirements.txt