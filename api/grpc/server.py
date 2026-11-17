# INTENTIONALLY VULNERABLE gRPC server - demo only.
import grpc, subprocess, sqlite3
from concurrent import futures
import user_pb2, user_pb2_grpc

class Svc(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, req, ctx):
        row = sqlite3.connect("app.db").execute("SELECT * FROM u WHERE id=" + req.id).fetchone()   # SQLi
        return user_pb2.User(id=req.id, name=row[1], password=row[2], ssn=row[3])
    def Exec(self, req, ctx):
        return user_pb2.ExecReply(output=subprocess.getoutput(req.cmd))                             # RCE

s = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
user_pb2_grpc.add_UserServiceServicer_to_server(Svc(), s)
s.add_insecure_port("[::]:50051")                                                                   # no TLS
s.start(); s.wait_for_termination()
