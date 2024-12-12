# Project Setup

## Create and Activate a Virtual Environment

### Step 1: Create the Virtual Environment

```bash
python -m venv env
```

### Step 2: Activate the Virtual Environment

On **Windows**, use:

```bash
env\Scripts\activate
```

On **Linux/MacOS**, use:

```bash
source env/bin/activate
```

## Install Dependencies

Install `fastapi`:

```bash
pip install fastapi
```

Install `uvicorn` with the standard dependencies:

```bash
pip install uvicorn[standard]
```

## Run the Application

Start the application using `uvicorn`:

```bash
uvicorn main:app --reload
```
