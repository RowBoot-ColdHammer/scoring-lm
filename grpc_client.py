import grpc
from proto import credit_scoring_pb2
from proto import credit_scoring_pb2_grpc

class CreditScoringClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = credit_scoring_pb2_grpc.CreditScoringServiceStub(self.channel)
    
    def score_credit(self, age, income, education, work, car):
        """Send credit scoring request to gRPC server"""
        request = credit_scoring_pb2.CreditRequest(
            age=age,
            income=income,
            education=education,
            work=work,
            car=car
        )
        
        try:
            response = self.stub.Score(request)
            return {
                'approved': response.approved,
                'score': response.score,
                'message': response.message
            }
        except grpc.RpcError as e:
            return {
                'approved': False,
                'score': 0.0,
                'message': f"gRPC error: {e.details()}"
            }
    
    def close(self):
        """Close the gRPC channel"""
        self.channel.close()

# Example usage
if __name__ == '__main__':
    client = CreditScoringClient()
    
    # Test with sample data
    result = client.score_credit(
        age=35,
        income=50000.0,
        education=True,
        work=True,
        car=True
    )
    
    print(f"Credit Decision: {'Approved' if result['approved'] else 'Rejected'}")
    print(f"Confidence Score: {result['score']:.2f}")
    print(f"Message: {result['message']}")
    
    client.close()