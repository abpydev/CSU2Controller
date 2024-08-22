import csu2controller

my_controller = csu2controller.CSU2Controller()
my_controller.connect()

resp = my_controller.query_ok()

print(resp)