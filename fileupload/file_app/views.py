from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
import PyPDF2
import tabula
import os


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
   
    if file_serializer.is_valid():

      file_serializer.save()
      nomeArquivo = file_serializer.data['file']
      
      df = tabula.read_pdf("../fileupload"+nomeArquivo)
      df.head()
      tabula.convert_into("../fileupload"+nomeArquivo, "media/resultado.xls", output_format="xls")

      return Response("/media/resultado.xls", status=status.HTTP_201_CREATED)

    else:

      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)