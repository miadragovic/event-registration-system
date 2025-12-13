# FastAPI Backend – Azure Deployment

This project is a backend web application built with **FastAPI** and served using **Uvicorn**.  
The application is deployed on **Azure App Service (Linux)** and connected to **GitHub** for continuous deployment.  
It can also be run locally for development and testing purposes.


## Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- Azure App Service (Linux)
- Git & GitHub

---

**Clone the repo**:
    ```
    git clone https://github.com/your-team/event-registration-api.git
    cd event-registration-api
    ```

**Create a virtual environment:** 
    ```
    python -m venv venv
    source venv/bin/activate   # macOS / Linux
    venv\Scripts\Activate      # Windows
    ```


**Install dependencies** 
    ```
    pip install -r requirements.txt
    ```

**Run pytest**
    ```
    pytest
    
    ```        
        


**Run the appliation:**
    ```
    uvicorn app.main:app --reload
    ```
**application available at:**
http://127.0.0.1:8000

**Admin login credentials:**
Local (Running on your machine)

Email: admin@gmail.com

Password: 12345

Cloud (Azure Deployment)

Email: fairouz3@gmail.com

Password: 12345

Note: These credentials are for development/testing purposes only.
In a production environment, credentials should be stored securely using environment variables or Azure Key Vault.

**Azure deployment details**
The application is deployed on Azure App Service (Linux).

Deployment is connected directly to GitHub.

On each push to the connected branch, Azure pulls the latest code and redeploys the application.

