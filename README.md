# Package Request Form Application

This application is a web-based form built with Streamlit and Python, designed to gather package request information and store it in a SharePoint list.

## Features

- User-friendly form interface for package request submission
- Sidebar for viewing previous requests
- Integration with SharePoint for data storage

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.6 or later.
- You have installed the necessary Python packages: `streamlit`, `python-dotenv`, and `sharepoint`.

## Environment Variables

This application uses the following environment variables:

- `CLIENT_ID`: Your SharePoint client ID.
- `CLIENT_SECRET`: Your SharePoint client secret.
- `TENANT_ID`: Your SharePoint tenant ID.

These should be stored in a `.env` file in the root directory of the project.

## Running the Application

To run the application, navigate to the project directory in your terminal and run the following command:

```bash
streamlit run web.py
```

This will start the Streamlit server and the application will be accessible at `localhost:8501` in your web browser.

## Contributing

If you want to contribute to this project, please fork the repository and create a pull request, or open an issue for any bugs or feature requests.

## License

This project uses the following license: MIT License.

