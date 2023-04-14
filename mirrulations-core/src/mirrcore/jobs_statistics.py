DOCKETS_DONE = "num_dockets_done"
DOCUMENTS_DONE = "num_documents_done"
COMMENTS_DONE = "num_comments_done"
ATTACHMENTS_DONE = 'num_attachments_done'
PDF_ATTACHMENTS_DONE = 'num_pdf_attachments_done'
EXTRACTIONS_DONE = 'num_extractions_done'


class JobStatistics:

    def __init__(self, cache):
        self.cache = cache

        self._check_keys_exist()

    def _check_keys_exist(self):
        keys = [DOCKETS_DONE, DOCUMENTS_DONE, COMMENTS_DONE, ATTACHMENTS_DONE,
                PDF_ATTACHMENTS_DONE, EXTRACTIONS_DONE]
        for key in keys:
            if not self.cache.exists(key):
                self.cache.set(key, 0)

    def get_jobs_done(self):
        dockets = int(self.cache.get(DOCKETS_DONE))
        documents = int(self.cache.get(DOCUMENTS_DONE))
        comments = int(self.cache.get(COMMENTS_DONE))
        attachments = int(self.cache.get(ATTACHMENTS_DONE))
        pdfs = int(self.cache.get(PDF_ATTACHMENTS_DONE))
        extractions = int(self.cache.get(EXTRACTIONS_DONE))

        return {
            'num_jobs_done': dockets + documents + comments + attachments +
            extractions,

            DOCKETS_DONE: dockets,
            DOCUMENTS_DONE: documents,
            COMMENTS_DONE: comments,
            ATTACHMENTS_DONE: attachments,
            PDF_ATTACHMENTS_DONE: pdfs,
            EXTRACTIONS_DONE: extractions
        }

    def increase_jobs_done(self, job_type, is_pdf=False):
        """
        increment the cache counter (currently redis) for the given job type
        when completed

        :param job_type: the type of job completed
        :param is_pdf: whether an attachment completed is a pdf
        """
        if job_type == "dockets":
            self.cache.incr(DOCKETS_DONE)
        elif job_type == 'documents':
            self.cache.incr(DOCUMENTS_DONE)
        elif job_type == 'comments':
            self.cache.incr(COMMENTS_DONE)
        elif job_type == 'attachment':
            self.cache.incr(ATTACHMENTS_DONE)
            if is_pdf:
                self.cache.incr(PDF_ATTACHMENTS_DONE)

    def increase_extractions_done(self):
        """
        Not a job being completed in the client
        """
        self.cache.incr(EXTRACTIONS_DONE)
