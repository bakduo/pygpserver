#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#############################################################################
#                                                                           #
#   Scripts de configuracion para Server tomar los datos de las             # 
#   peticiones enviadas desde la pagina por medio de un formulario          #
#   fue construido utilizando varios codigos de python desde los foros y    #
#   wikis aun esta en desarrollo.                                           #
#   Copyright (C) 2013 linuxknow@gmail.com                                  #
#                                                                           #
#   This program is free software: you can redistribute it and/or modify    #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   This program is distributed in the hope that it will be useful,         #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>    #
#                                                                           #
#############################################################################

"""
import os
import sys
import cgi
import BaseHTTPServer
import subprocess
from urlparse import urlparse, parse_qs

class RequestHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        """Tomamos los parametros desde POST con uso de cgi"""
        
        form = cgi.FieldStorage(
        fp=self.rfile, 
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
        'CONTENT_TYPE':self.headers['Content-Type'],
        })

        arch=""
        di=""
        distro=""
        nombreiso=""
        filesystem=""
        area=""
        repo=""
        desktop="" 
        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self._post_status())
       

        for field in form.keys():
            if field == "arch":
               arch=form[field].value
               print arch
            elif field== "di":
               di=form[field].value
               print di
            elif field == "distro":
               distro=form[field].value
               print distro
            elif  field=="area":
               area=form[field].value
               print area
            elif field=="repoextra":
               repo=form[field].value
               print repo
            elif field=="desktop":
               desktop=form[field].value
               print desktop
            elif field=="nombreiso":
               nombreiso=form[field].value
               print nombreiso
            elif field=="filesystem":
               filesystem=form[field].value
               print filesystem

            print "clave=%s valor=%s" % (field, form[field].value)

        str="cd /usr/src/lihuen/Lihuen/testing;./configLihuen.sh %s %s http://%s/debian %s %s %s %s %s" % (arch,nombreiso,repo,desktop,filesystem,di,area,distro)
        p = subprocess.Popen(str, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        print output

        return

    def do_GET (self):
        """Tomamos los parametros desde GET """

        parametros_from_get=parse_qs(urlparse(self.path).query)

        """ Los parametros los pasamos a un diccionario para tener un string simple"""

        parametros_to_string=dict((clave,valor if len(valor)>1 else valor[0] )
                           for clave,valor in parametros_from_get.iteritems() )

        """ Imprimimos los valores para debug"""

        for clave, valor in parametros_to_string.items():
           print "%s=%s" % (clave, valor)

        """ Enviamos un 200 ok"""
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self._get_status())
        return

    def _post_status (self):
        """ informamos del estado """
        return "Procesamiento en proceso: %s" % ("%01.2f, %01.2f, %01.2f" % os.getloadavg())

    def _get_status (self):
        """ informamos del estado """
        return "Status:\n" \
               "--\n" \
               "Load average: %s\n" % \
               ("%01.2f, %01.2f, %01.2f" % \
                           os.getloadavg())            

def main (args):
    httpd = BaseHTTPServer.HTTPServer(('localhost', 8000), RequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
