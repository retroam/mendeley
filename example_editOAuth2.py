



from mendeley_client import *
from auth import *
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON
from settings import defaults


user = 'rka2p'

redirect_uri = 'http://0.0.0.0:5000/api/v1/addons/mendeley/callback/%s/' % user
code = ''

MEND = MendeleyClient(defaults.CLIENT_ID, defaults.CLIENT_SECRET, {"host":host})
session = OAuth2Session(
        mendeley_settings.CLIENT_ID,
        redirect_uri=redirect_uri
    )
token = session.fetch_token(
        OAUTH_ACCESS_TOKEN_URL,
        client_secret=mendeley_settings.CLIENT_SECRET,
        code=code,
    )

access_token = tokens_store.get_access_token(account_name)
MEND.set_access_token(access_token)

# library = client.library()
# documentId = library['document_ids']
#
# doc_meta = []
#
# for idx in range(0,len(documentId)-1):
#     meta = client.document_details(documentId[idx])
#     doc_meta.append({
#         "id": meta['id'],
#         "title":meta['title'],
#         "publisher": meta['published_in'],
#         "type": "journal",
#     })
#     # print "TITLE: " + doc_meta['title'] + "\n"
# print doc_meta
# bib_source = CiteProcJSON(doc_meta)
#
# bib_style = CitationStylesStyle('harvard1')
# bibliography = CitationStylesBibliography(bib_style, bib_source,formatter.plain)
#
# print bibliography.bibliography()
#
# # print('')
# # print('Bibliography')
# # print('-----------')
# # for item in bibliography.bibliography():
# #     print (str(item))
