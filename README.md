
# AdidasMonitor

AdidasMonitor is a Python script designed to monitor the availability of product sizes on the Adidas website. It uses proxies to make requests and log the available sizes of a specified product.

## Features

- Monitors availability of product sizes on Adidas.
- Uses proxies to make requests.
- Logs available sizes and any changes in availability status.
- Configurable product ID and request intervals.

## Requirements

The required Python packages are listed in `requirements.txt`:

```plaintext
certifi==2024.6.2
charset-normalizer==3.3.2
idna==3.7
requests==2.32.3
tls-client==1.0.1
typing_extensions==4.12.2
urllib3==2.2.2
```

To install the required packages, run:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/DieserLaurenz/AdidasMonitor.git
cd AdidasMonitor
```

2. Configure the script:
   - Set the `PRODUCT_ID` to the desired Adidas product ID in `adidasmonitor.py`.
   - Set `USE_PROXIES` to `True` if you want to use proxies, and make sure to add your proxies to `data/proxies.txt`.

3. Run the script:

```bash
python AdidasMonitor/adidasmonitor.py
```

## Logging

The script logs information to `app.log` and the console. It logs the available sizes and any changes in availability status.

## File Structure

- `AdidasMonitor/adidasmonitor.py`: The main script for monitoring product availability.
- `requirements.txt`: A list of required Python packages.
- `app.log`: Log file (generated during runtime).
- `data/proxies.txt`: File containing proxy information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests.
