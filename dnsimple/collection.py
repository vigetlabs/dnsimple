class Collection(object):

    def to_dict(self):
        """
        Return the dict representation of the collection.

        Returns
        -------
        dict
            Dictionary representation of all instances in the collection
        """
        return [model.to_dict() for model in self.all()]

    def __iter__(self):
        """
        Return an iterator for use in ``for ... in ...`` statements.

        Returns
        -------
        listiterator
            Iterator instance wrapping return value of ``all()``
        """
        return iter(self.all())
