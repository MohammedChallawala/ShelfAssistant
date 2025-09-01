from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Import routers
from .routes import products, vision, llm

app = FastAPI(
    title="ShelfAssistant API",
    description="Smart shelf system using IoT devices + local LLM for supermarket assistance",
    version="1.0.0"
)

# Include routers
app.include_router(products.router)
app.include_router(vision.router)
app.include_router(llm.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ShelfAssistant API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #0066cc; }
            .url { font-family: monospace; background: #e8e8e8; padding: 2px 6px; border-radius: 3px; }
            .description { color: #666; margin-top: 5px; }
            .links { margin: 20px 0; }
            .links a { display: inline-block; margin: 5px 10px 5px 0; padding: 10px 15px; 
                       background: #0066cc; color: white; text-decoration: none; border-radius: 5px; }
            .section { margin: 30px 0; }
            .section h2 { color: #333; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }
        </style>
    </head>
    <body>
        <h1>🛒 ShelfAssistant API</h1>
        <p>Welcome to your AI-powered shelf assistant API! Use the endpoints below to interact with the system.</p>
        
        <div class="links">
            <a href="/docs" target="_blank">📚 Interactive API Docs</a>
            <a href="/redoc" target="_blank">📖 ReDoc API Docs</a>
            <a href="/health">💚 Health Check</a>
        </div>
        
        <div class="section">
            <h2>📦 Products Management</h2>
            <p>CRUD operations for managing shelf products</p>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/products</div>
                <div class="description">Get all products with pagination and search</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/products</div>
                <div class="description">Create a new product</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/products/{id}</div>
                <div class="description">Get a specific product by ID</div>
            </div>
            
            <div class="endpoint">
                <div class="method">PUT</div>
                <div class="url">/products/{id}</div>
                <div class="description">Update a product by ID</div>
            </div>
            
            <div class="endpoint">
                <div class="method">DELETE</div>
                <div class="url">/products/{id}</div>
                <div class="description">Delete a product by ID</div>
            </div>
        </div>
        
        <div class="section">
            <h2>👁️ Vision Recognition</h2>
            <p>YOLOv8-based shelf product detection (coming soon)</p>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/vision/detect</div>
                <div class="description">Detect products in shelf images (TODO: Implement YOLOv8)</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🤖 LLM Q&A</h2>
            <p>Local LLM inference for product questions (coming soon)</p>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="url">/llm/ask</div>
                <div class="description">Ask questions about products (TODO: Implement local LLM)</div>
            </div>
        </div>
        
        <h2>Getting Started:</h2>
        <p>1. Use the interactive docs at <a href="/docs">/docs</a> to test the API endpoints</p>
        <p>2. Products endpoints are fully functional with SQLite database</p>
        <p>3. Vision and LLM endpoints are placeholders for future implementation</p>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "ok", "service": "ShelfAssistant API", "version": "1.0.0"}
