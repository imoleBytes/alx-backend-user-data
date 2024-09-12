#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ adds a user to db and returns the user obj"""
        user = User(email=email, hashed_password=hashed_password)

        self._session.add(user)
        self._session.commit()

        added_user = self._session.query(User).filter_by(email=email).first()
        return added_user

    def find_user_by(self, **kwargs) -> User:
        """
        This method takes in arbitrary keyword arguments and returns the
        first row found in the users table as filtered by the method's input
        arguments.
        """
        if kwargs is None:
            raise InvalidRequestError
        for k in kwargs.keys():
            if k not in User.__dict__:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound
        return user
        # for k, v in kwargs.items():
        #     if k not in User.__dict__:
        #         raise InvalidRequestError

        #     for user in users:
        #         if getattr(User, k) == v:
        #             return user
        # raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        takes as argument a required user_id integer and
        arbitrary keyword arguments, and returns None.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError

        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise ValueError
            setattr(user, k, v)
        self._session.commit()
