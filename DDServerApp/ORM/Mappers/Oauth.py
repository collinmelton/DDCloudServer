'''
Created on Dec 3, 2015

@author: cmelton

These classes are modeled after the Oauth1 server example at https://flask-oauthlib.readthedocs.org/en/latest/oauth1.html

'''

from DDServerApp.ORM import orm,Column,relationship,String,Integer, PickleType, Float,ForeignKey,backref,TextReader, joinedload_all
from DDServerApp.ORM import BASE_DIR, Boolean
from DDServerApp.ORM.Mappers import Instance
from User import User
from werkzeug.security import gen_salt

class Client(orm.Base):
    '''
    A client is the app which want to use the resource of a user. It is suggested that the client is registered by a user on your site, but it is not required.

    The client should contain at least these information:
    
    client_key: A random string
    client_secret: A random string
    redirect_uris: A list of redirect uris
    default_redirect_uri: One of the redirect uris
    default_realms: Default realms/scopes of the client
    But it could be better, if you implemented:
    
    validate_realms: A function to validate realms
    
    '''
    id = Column(Integer,primary_key=True)
    
    # human readable name, not required
    name = Column(String)

    # human readable description, not required
    description = Column(String)

    # creator of the client, not required
    user_id = Column(ForeignKey('user.id'))
    
    # required if you need to support client credential
    user = relationship(User)

    instance_id = Column(Integer, ForeignKey('instance.id'))
    instance = relationship(Instance, backref = "instances")

    client_key = Column(String, index=True)
    client_secret = Column(String, unique=True, index=True, nullable=False)

    _realms = Column(String)
    _redirect_uris = Column(String)
    
    def __init__(self, name, description, user, realms, redirect_uris, instance):
        '''
        Constructor
        '''
        self.name = name
        self.description = description
        self.user = user
        self.client_key = gen_salt(25)
        self.client_secret = gen_salt(25)
        self._realms = " ".join(realms)
        self._redirect_uris = " ".join(redirect_uris)
        self.instance = instance

    def getClientCredentials(self):
        return str({"client_key":self.client_key, "client_secret":self.client_secret})

    def createAccessToken(self, SESSION):
        '''
        Creates an access token for this client.
        '''
        token = gen_salt(25)
        secret = gen_salt(25)
        return AccessToken(self, self.user, token, secret, self._realms)    

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_realms(self):
        if self._realms:
            return self._realms.split()
        return []
    
    @staticmethod
    def findFirst(client_key, session):
        '''
        Returns the first client that matches the client_key
        '''
        return session.query(Client).filter_by(client_key=client_key).first()
#         return Client.query
    
class RequestToken(orm.Base):
    '''
    Request token is designed for exchanging access token. Verifier token is designed to verify the current user. It is always suggested that you combine request token and verifier together.

    The request token should contain:
    
    client: Client associated with this token
    token: Access token
    secret: Access token secret
    realms: Realms with this access token
    redirect_uri: A URI for redirecting
    The verifier should contain:
    
    verifier: A random string for verifier
    user: The current user
    '''
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship(User)

    client_key = Column(String, ForeignKey('client.client_key'), nullable=False,)
    client = relationship(Client)

    # access token and access token secret
    token = Column(String, index=True, unique=True)
    secret = Column(String, nullable=False)

    # random verifier string
    verifier = Column(String)

    redirect_uri = Column(String)
    _realms = Column(String)

    @property
    def realms(self):
        if self._realms:
            return self._realms.split()
        return []
    
    @staticmethod
    def findFirst(token, session, verifier=None):
        '''
        Returns the first token that matches the token and verifier (if specified).
        '''
        if verifier != None:
            session.query(RequestToken).filter_by(token=token).first()
        else:
            session.query(RequestToken).filter_by(verifier=verifier, token=token).first()

class Nonce(orm.Base):
    '''
    Timestamp and nonce is a token for preventing repeating requests, it can store these information:

    client_key: The client/consure key
    timestamp: The oauth_timestamp parameter
    nonce: The oauth_nonce parameter
    request_token: Request token string, if any
    access_token: Access token string, if any
    The timelife of a timestamp and nonce is 60 senconds, put it in a cache please. Here is an example in SQLAlchemy:
    '''
    id = Column(Integer, primary_key=True)

    timestamp = Column(Integer)
    nonce = Column(String)
    client_key = Column(String, ForeignKey('client.client_key'), nullable=False)
    client = relationship('Client')
    request_token = Column(String)
    access_token = Column(String)
    
    @staticmethod
    def findFirst(client_key, timestamp, nonce, request_token, access_token, session):
        return session.query(Nonce).filter_by(client_key=client_key, timestamp=timestamp, 
                                     nonce=nonce, request_token=request_token, 
                                     access_token=access_token).first()
    
class AccessToken(orm.Base):
    '''
    An access token is the final token that could be use by the client. Client will send access token everytime when it need to access resource.
    A access token requires at least these information:

    client: Client associated with this token
    user: User associated with this token
    token: Access token
    secret: Access token secret
    realms: Realms with this access token
    '''
    id = Column(Integer, primary_key=True)
    client_key = Column(String, ForeignKey('client.client_key'), nullable=False)
    client = relationship('Client')

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')

    token = Column(String)
    secret = Column(String)

    _realms = Column(String)

    def __init__(self, client, user, token, secret, realms):
        self.client = client
        self.user = user
        self.token = token
        self.secret = secret
        self._realms = realms

    def __str__(self):
        return "token: "+self.token+", secret: "+ self.secret

    @property
    def realms(self):
        if self._realms:
            return self._realms.split()
        return []
    
    @staticmethod
    def findFirst(client_key, token, session):
        if token != None:
            return session.query(AccessToken).filter_by(client_key=client_key, token=token).first()
        return session.query(AccessToken).filter_by(client_key=client_key).first()