import grpc
from concurrent import futures
import joblib
import sqlite3
import os
from typing import Dict, Any
from proto import credit_scoring_pb2
from proto import credit_scoring_pb2_grpc

# Path configurations
project_root = os.path.dirname(__file__)
data_dir = os.path.join(project_root, 'data')
db_dir = os.path.join(data_dir, 'db')
models_dir = os.path.join(data_dir, 'models')

sqlite_db = os.path.join(db_dir, 'test.db')
model = joblib.load(os.path.join(models_dir, 'model.pkl'))

class CreditScoringService(credit_scoring_pb2_grpc.CreditScoringServiceServicer):
    def __init__(self):
        # Initialize database table if not exists
        self._init_database()
        self.host = os.getenv('GRPC_HOST', 'localhost')
        self.port = int(os.getenv('GRPC_PORT', '50051'))
    
    def _init_database(self):
        """Initialize database table if it doesn't exist"""
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                income REAL,
                education BOOLEAN,
                work BOOLEAN,
                car BOOLEAN,
                "default" INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    
    def _insert_data(self, request: Dict[str, Any], default_pred: int):
        """Insert customer data into database"""
        conn = sqlite3.connect(sqlite_db)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO customers (age, income, education, work, car, "default")
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                request['age'],
                request['income'],
                request['education'],
                request['work'],
                request['car'],
                default_pred
            ))
            conn.commit()
        finally:
            conn.close()
    
    def _calculate_features(self, request) -> list:
        """Extract features from request"""
        return [
            request.age,
            request.income,
            request.education,
            request.work,
            request.car
        ]
    
    def Score(self, request, context):
        """gRPC method to score credit application"""
        try:
            # Convert request to dictionary for easier handling
            request_dict = {
                'age': request.age,
                'income': request.income,
                'education': request.education,
                'work': request.work,
                'car': request.car
            }
            
            # Calculate features and make prediction
            features = self._calculate_features(request)
            approved = not model.predict([features])[0].item()
            default_pred = 1 if approved else 0
            
            # Insert into database
            self._insert_data(request_dict, default_pred)
            
            confidence = model.predict_proba([features])[0][0] if hasattr(model, 'predict_proba') else 0.8
            
            return credit_scoring_pb2.CreditResponse(
                approved=approved,
                score=float(confidence),
                message="Credit scoring completed successfully"
            )
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error processing request: {str(e)}")
            return credit_scoring_pb2.CreditResponse(
                approved=False,
                score=0.0,
                message=f"Error: {str(e)}"
            )

def serve():
    """Start gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    credit_scoring_pb2_grpc.add_CreditScoringServiceServicer_to_server(
        CreditScoringService(), server
    )
    
    # You can change the port as needed
    server.add_insecure_port('[::]:50051')
    
    print("Starting gRPC server on port 50051...")
    server.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop(0)

if __name__ == '__main__':
    serve()