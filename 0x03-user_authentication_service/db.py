#!/usr/bin/env python3
"""
db mod
"""
from sqlalchemy import create_engine
from sqlalchemy.exit.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    DB class"""
    
    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("splite:///a.db",
                                     echo=self.False)
        Base.metadata.drop_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memorized session obj"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User:
        """
        create a user obj & save it to db
        Args:
            email (str): user's email address
            hashed_password (str): password hashed by bcrypt hashpw
        Return:
            Newly created user obj
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Return a user who has an atr matching the atr's passed
        as args
        Args:
            attributes (dict): a dictiornary of atr to match user
        Return:
            matching user ot raise error
        """
        all_users = self._session.query(User)
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise InvalidRequestError
            for usr in all_users:
                if getattr(usr, k) == v:
                    return usr
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attr's
        Args:
            user_id (int): user's id
            kwargs (dict): dict of key, value pairs representing the
                            attr's to update & the values to update
                            them with
        Return:
            No return value
        """
        try:
            usr = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for k, v in kwargs.items():
            if hasattr(usr, k):
                setattr(usr, k, v)
            else:
                raise ValueError
        self._session.commit()
