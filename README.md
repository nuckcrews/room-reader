# Room Reader

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

   ```bash
   $ cd room-reader
   ```

4. Create a new virtual environment

   ```bash
   $ virtualenv virt
   $ source virt/bin/activate
   ```

5. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

## Applications

#### General Room Reader

```bash
./run.sh
```

#### Excel Pilot

```bash
./excel.sh
```