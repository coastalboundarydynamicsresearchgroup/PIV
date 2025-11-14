import camera as c
import time as t
import matplotlib.pyplot as plt



def battery_test(file_path = "PythonScripts/Scripts/Graham/Test_Logs/batterylevel.txt",count_per_test = 25, time_between_tests = 1,timeout = 2000):
    with open(file_path, "a") as file1:
                file1.write(f"\nRunning Test {t.ctime()} - {count_per_test} photo(s) per test - {time_between_tests} second(s) inbetween - {timeout}ms camera timeout\n\n")
                file1.close
    camera = c.EasyCamera("My Camera")
    testnum = 0
    failures = []
    while True:
        try: 
            testnum += 1
            camera.issues = 0
            camera.clear_folder()
            camera.take_photos(count=count_per_test, time_between=time_between_tests, delay = 0,timeout = timeout)
            with open(file_path, "a") as file1:
                file1.write(f"Test {testnum} - {t.ctime()}\t: The camera failed to capture\t{(camera.issues/count_per_test)*100}% of the time\n")
                file1.close
        except:
              break
    plt.plot(failures)
    with open(file_path, "a") as file1:
        for i in failures:
            file1.write(i)

    




def graph():
      with open("PythonScripts/Scripts/Graham/Test_Logs/batterylevel.txt", "r") as file1:
        logs = file1.readlines()[3:]
        data = []
        for i in logs:
            data.append(float(i[65:][:5].replace("\t","").replace(" ","").replace("%","")))
        plt.plot(data)
        plt.show()

def timeout_test(file_path = "PythonScripts/Scripts/Graham/Test_Logs/timeoutlog.txt",count_per_test = 25, time_between_tests = 1):
   
    with open(file_path, "a") as file1:
                file1.write(f"\nRunning Test {t.ctime()} - {count_per_test} photo(s) per test - {time_between_tests} second(s) inbetween\n\n")
                file1.close
    camera = c.EasyCamera("My Camera")
    for timeout in reversed(range(50,1250,50)):
        camera.issues = 0
        camera.clear_folder()
        camera.take_photos(count=count_per_test, time_between=time_between_tests, delay = 0,timeout = timeout)
        with open(file_path, "a") as file1:
            file1.write(f"With a timeout of {timeout}ms : The camera failed to capture\t{(camera.issues/count_per_test)*100}% of the time\n")
            file1.close


# timeout_test() 
# battery_test()
graph()




