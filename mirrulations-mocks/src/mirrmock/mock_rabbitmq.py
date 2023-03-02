class MockRabbit:

    def __init__(self):
        self.jobs = []

    def add(self, job):
        self.jobs.append(job)

    def size(self):
        return len(self.jobs)

    def get(self):
        return self.jobs.pop(0)
