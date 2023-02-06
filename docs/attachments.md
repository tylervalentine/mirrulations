# Attachments

### Acquiring Attachments
- The process for acquiring links to attachments
1. Navigate to a comments["relationships"]["attachments"]["links"]["related"]
2. In order to visit this link we have to use another api_call to access the links to the attachments
3. From this related link we then must iterate over the list of files attached to the comment
    
    File Types include: ```bmp, docx, gif, jpg, jpeg, pdf, png, pptx, rtf, sgml, tif, tiff, txt, wpd, xlsx, xml```

4. We then download each file to disk, as well as write the path of the attachment to our mongodb


### Attachments Storage
- Attachments are being stored on disk under their respective Agency Name Abbreviation and respective comment the attachment came from. 

Ex: ```"OSHA/OSHA-H371-2006-0932-0879/22899605_0.pdf"```

*Breakdown*
- ```<AgencyID>/<CommentID>/<job_id>.<file_type>```



## Breakdown of Attachments by File Type
- Current Attachment Count: 207.9k

The following summary of file types was accumulated from our smaller sample of attachments we have in mongo 

Script to generate this data can be found here:

[attachment_types.py](https://github.com/cs334s23/mirrulations_attachments_exploration/blob/main/src/attachment_types.py)
| File Type     | Count |
| ----------- | ----------- |
| .pdf      | 176672       |
| .docx   | 18676       |
| .jpg      | 5803      |
| .png   | 2705        |
| .xlsx  | 819       |
| .txt     | 559       |
| .tif   | 467        |
| .doc   | 262        |
| .rtf      | 214      |
| .pptx   | 80       |
| .wpd      |37       |
| .gif   | 28       |
| .bmp   | 10       |
| .htm, .wav, .zip , .ppt  | <10   |

