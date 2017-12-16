****************************************
FIWARE-IoT Client installation tutorial
****************************************

.. contents::
   :local:
   :depth: 3


.. _introduction:

Introduction
====================


.. begin-conceptTheory

Conceptual Theory
--------------------

A platform `FIWARE <https://www.fiware.org>`__ presents an environment based on the cloud computing platform `OpenStack <https://www.openstack.org>`__ with some modifications as well as with the addition of other components. It features a set of standardized APIs that, among other things, make it easier to communicate with the Internet of Things (IoT) and manipulate context information. It facilitates analysis of large volumes of data and provision of real-time averages, providing facilities for manipulating context information, real-time event analysis, information gathering from sensors and actuator action, access control among many other features.

These sets of functionalities are grouped in the platform in the form of chapters, each of them consisting of a set of GEs (Generic Enablers), nomenclature given to components within the platform.

Regarding IoT applications, the platform provides GEs that allow "things" to become available, searchable, accessible and usable context resources, enabling the interaction of FIWARE Apps with real-world objects. The "things" represent any physical object, living organism, person or concept of interest from the perspective of an application and its parameters are totally or partially attached to sensors, actuators (or a combination of these). The platform helps in abstracting the complexity and high fragmentation of IoT technologies and deployment scenarios.


Understanding some concepts is critical to using the FIWARE APIs and, consequently, tools that make use of them. So, below will be defined some concepts that facilitate the understanding of what will be presented during this tutorial.

**Device:** It refers to a hardware entity, component or system. It is responsible for measuring or influencing the properties of a thing/group of things (or both, concurrently). Sensors and actuators are examples of devices.

**End-Node:** The term is used in documentation for complex physical devices with multiple sensors and actuators, such as a complex Arduino-based system. Devices may use proprietary or standardized communication protocols, which can be natively sent to Backend GEs or translated into another standardized or proprietary protocol in IoT Gateways, such as the conversion of these specific protocols to OMA Next Generation Services Interface (NGSI) specification (OMA, 2012) that can be performed in FIWARE GEs, for instance. An Arduino or Raspberry Pi are examples of IoT End-Nodes.

**IoT Resource:** An IoT Resource refers to a computational element that provides access to sensor/actuator devices. An information model for describing IoT features can include context information, such as location, accuracy and status information, for example. Data at IoT resources consist not only of the measured data, but also of context information, such as data type, time instant, measurement accuracy and the sensor from which measurement was performed. IoT resources can be addressed using a uniform addressing scheme and are usually hosted on the device but also have a logical representation on the IoT Backend level.

**Thing:** It concerns any object, person, or place in the real world. They are represented as virtual things and, in their representation, they have an entity ID, a type and several attributes. Sensors can be modeled as virtual things, but things in the real world, whether concrete or abstract (such as rooms, people and groups), can also be modeled as virtual things. Data at the level of things consist of descriptions of things and their attributes, and may also include information on how the data were obtained through meta data.

**NGSI Context-Entity:** IoT End-Nodes, IoT Resources and "Things" are rep- resented as NGSI Context Entities in the GE Context Broker of the data chapter, so developers need to learn only the same API from that GE, used for context information, to also manage application information IoT. Sensor measurement information can be obtained by reading the attributes of these entities, while actuating commands in actuators can be done by updating specific attributes that represent commands in them.

**Service e Service-Path:** They are used to define the scope used to execute requests and operations, making the necessary operations performed on devices and entities with certain unique IDs within a specific scope, located together with the Service and Service-Path values defined in time of recording and sending measurements to devices.

.. end-conceptTheory



.. _environmentInstalation:

Installation of environment
======================

The environment is made up of two components: the back-end using Docker, and the front end using the FIWARE-IoT-Client.


Installation of back-end: Docker
-----------------------------

.. begin-docker

To prepare the environment for the execution of the tutorial, we must first run the GEs that will be necessary for the creation of IoT applications using FIWARE. For this, the architecture presented in the figure below, composed of the main components necessary to create applications that use context manipulation and IoT resources in the platform was planned.

.. image:: https://github.com/rahul606/FIWARE-IoT-Tutorial/blob/master/extras/fiware_components_deploy.png
Figure 01 - Architecture of FIWARE components selected for the tutorial


It is possible to identify components responsible for communicating with devices (IDAS), storage and manipulation of context information (Orion Context Broker), communication with databases for storage of measurements (Cygnus) and the databases used to perform this persistence , and a * MySQL * and a * MongoDB * database were selected for the execution of the tutorial, as well as the FIWARE component responsible for storing historical data, allowing the storage and query of aggregated historical data (STH Comet).

In order to create the environment composed of all these components, the `Docker <https://www.docker.com>` __ tool was used, which allows, from the available images of the selected FIWARE components, to set configuration parameters well how the communication between these components will occur and how they will be accessible for use by applications.

NOTE: If there is already a configured and available environment that presents the components used by the tutorial and presented in the image above, you can skip the following steps to configure the environment on your machine.

Initially you need to install Docker on your machine if you do not already have it installed. The steps for the installation in your operating system can be accessed in the `link <https://www.docker.com/get-docker>` __.

You also need to install the docker-compose tool, which will allow the environment composed of all selected components to be easily executed. The steps for the installation can be accessed in the `link <https://docs.docker.com/compose/install>` __.

Having properly installed Docker and docker-compose, you're ready to run the environment. To do this, you should go to the directory where the tutorial repository was cloned, in which there is a file called `docker-compose.yml <https://github.com/rahul606/FIWARE-IoT-Tutorial/blob/master/deploy/full/docker-compose.yml> `__, and, from the command line of your operating system, run the command:

$ docker-compose up -d

This command will run all the components required to run the tutorial, and if no error message has been displayed, it should be running correctly.

To test whether the environment has been configured and running correctly, open your browser and go to address localhost:1026/version and a * JSON * should be returned showing the version of the Orion component running.



.. end-docker

Installation of front-end : FIWARE-IoT-Client-Python
----------------------------------------------------

Virtual environment configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To start, a directory should be created where the environment will be installed, and access it ::

$ mkdir my-directory
$ cd my-directory

After the directory is created, a Python virtual environment is created ::

$ python3 -m venv .my-environment

To activate it, we use the source command ::

$ source .my-environment/bin/activate

With the virtual environment already created, the installation of iPython is done by ::

$ (.my-environment) pip install ipython


Installing the FIWARE-IoT-Client library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the installation of the library, run the command ::

$ (.my-environment) pip install -e git+https://github.com/FIoT-Client/fiot-client-python.git#egg=fiotclient

For cases where the virtual environment is not used, the above command should be used with sudo ::

$ sudo pip install -e git+https://github.com/FIoT-Client/fiot-client-python.git#egg=fiotclient


And to test if the installation was done correctly, we do the Python import command ::


$ (.my-environment) ipython
>>> from fiotclient import iot


Installation of front-end: GUI Web
----------------------------------

.. begin-GUI

Coming soon!

.. end-GUI

.. _registerDevice:

Registering a device
====================

Using FIWARE-IoT-Client
-----------------------

Registering the device in the Fiware
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. begin-FIWAREIoTClient-register

Configure config.ini
""""""""""""""""""""

To start the registration of the device, we must first create a configuration file, however to facilitate the progress of the tutorial, there is a file
pre-programmed configuration in this `repository <` https://github.com/rahul606/FIWARE-IoT-Tutorial/blob/master/config.ini> `__,
in which from it the user can change the values of the addresses of the components of which he will use.



Creating Service and Service Path
"""""""""""""""""""""""""""""""""

After you configure config.ini, the next step is to create the Service and Service Path, using the previously installed fiotclient library. ::

$ (.my-environment) ipython
>>> from fiotclient import iot #import library 'fiotclient'
>>> client_iot = iot.FiwareIotClient('config.ini') #configure the components using config.ini
>>> client_iot.create_service('SERVICE_NAME', '/SERVICE_PATH') #creates the service by setting its name and path

NOTE: The service path must be preceded by a slash '/' and can not contain certain special characters such as underscore ('_').

After the service is created, there will be a confirmation message, along with a string, that must be saved together with the Service name and its Service Path to be used when registering a new device. The confirmation message is displayed this way: ::

{"status_code": 201,"api_key": 'API_KEY'}


Registering a device
""""""""""""""""""""

For the registration of a new device, first we must select in which Service and in which Service Path it will stay, in which it is done using the commands: ::

>>> client_iot.set_service('SERVICE_NAME', '/SERVICE_PATH')

Using previously saved values. With this, the next step is to assign the API_KEY to the device, using the command:


>>> client_iot.set_api_key('API_KEY')

After all the assignments are made, the next step is to register the device, which is defined by a JSON format file, where some examples of devices can be found in this `repository <https://github.com/rahul606/FIWARE-IoT-Tutorial/tree/master/examples/devices> `__.
It is recommended that the device files be saved in the same directory where the application will be running.

Finally, to register the device, the following command is used:: ::

>>> client_iot.register_device('CAMINHO_DEVICE', 'ID_DEVICE', 'ID_ENTITY')

having as arguments the directory in which the device file, the device id, and the entity id in which the device is relating respectively are saved. All of these values are contained in the device's JSON file.

To list the devices that are registered in this SERVICE, we use this command: ::

>>> client_iot.list_devices()

With this the next step is the configuration of the entity that will be relating to the device (s) of the application.

Configuring storage (registering databases in Orion)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creation of entity
""""""""""""""""""
For the creation of the entity, we must first import the methods related to the entity API access module from the fiotclient library, after which we must configure the entity's components using the config.ini file, and this step is done through these commands: ::

>>> from fiotclient import context
>>> client_context = context.FiwareContextClient('config.ini')

Once this is done, the assignment of the entity to SERVICE and to the desired SERVICE PATH is done using the following command: ::

>>> client_context.set_service('SERVICE_NAME', '/SERVICE_PATH')

To check the information for this entity, we use this command: ::

>>> client_context.get_entity_by_id('ID_ENTITY')


Connecting the entity with Cygnus
"""""""""""""""""""""""""""""""""

To connect the entity with Cygnus, we use the following command: ::

>>> client_context.subscribe_cygnus('ID_ENTITY', ['ATTR_01', ...])

The attributes are the id of the entity in which you want to connect with Cygnus, and the attributes of the devices.

With this, it is possible to send the data collected by the devices to a database, being a database in MySQL, MongoDB, etc.

And finally, to send and store the data history, we use the following command: ::

>>> client_context.subscribe_historical_data('ID_ENTITY', ['ATTR_01', ...])


Using the WEB GUI
-----------------

.. begin-WEB GUI-Register

Coming soon!

.. end-WEB GUi-Register


.. _programmingDevice:


Programming the device
======================

Arduino
-------

.. begin-programming-Arduino

In this example, a temperature and humidity sensor DHT21 AM2301 was used, in which the file is located in this `link <https://github.com/rahul606/FIWARE-IoT-Tutorial/blob/master/examples/arduino/FiwareDHT/FiwareDHT.ino> `__.


.. end-programming-Arduino


Raspberry Pi
------------

.. begin-programming-RaspberryPi

In this example, a temperature and humidity sensor DHT22 AM2302 was used, in which the file is located in this `link <https://github.com/rahul606/FIWARE-IoT-Tutorial/blob/master/examples/example_DHT2302.py> `__.

.. end-programming-RaspberryPi

.. _visualizeData:

Visualise the data
==================


Using Web GUI
--------------

.. begin-visualize-GUI


Coming soon!

.. end-visualize-GUI

Database Query
--------------


.. begin-visualize-Database

Coming soon!


.. end-visualize-Database

Mysql
-----

.. begin-visualize-mysql

When creating the Service, a database with the same name is used at the time of registration, but all in lowercase. For each registered entity, a table is also created in the database of its respective service, in the format "SERVICE_PATH" + "_" + "IDENTITY" + "_" + "TYPE_INTITY".

To access the database being used in the Service, the command:


.. code-block:: sql


   use DATABASE_NAME

Where 'DATABASE_NAME' must be replaced with the name of the database created for the service.

Then select the Service database, to check all the data registered in an entity is used this command:


.. code-block:: sql


 SELECT * FROM ENTITY_TABLE

Where 'ENTITY_TABLE' should be replaced by the name of the table created for the desired entity.

.. end-visualize-mysql

MongoDB
-------

.. begin-visualize-mongoDB


Coming soon!

.. end-visualize-mongoDB

ELK
---

.. begin-visualize-ELK

Coming soon!

.. end-visualize-ELK

Check the Orion
---------------

.. begin-visualize-Orion


Coming soon!

.. end-visualize-Orion
