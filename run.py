from app import create_app

if __name__ == "__main__":
    app = create_app("config")
    #uncomment when pushing to docker hub
    #app.run(debug=True,host='0.0.0.0', port=7001)  
    app.run(debug=True,host='127.0.0.1', port=9001)
    #app.run(debug=True,host='192.168.43.135', port=7001)

    
   
 