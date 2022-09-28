

class response_mk:
    
    def build_repsonse_many(self,many:list):
        response = []

        for row in many:
            response.append(dict(zip(row.keys(), row)))

        return response
