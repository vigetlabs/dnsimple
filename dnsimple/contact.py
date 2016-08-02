from .model import Model

class Contact(Model, object):

    def update(self, attributes):
        self.assign(attributes)

        response = self.request.put(
            'contacts/{0}'.format(self.id),
            {'contact': attributes}
        )

        return response.was_successful()

    def delete(self):
        response = self.request.delete('contacts/{0}'.format(self.id))
        return response.was_successful()
