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
from subprocess import call
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
       
        """
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')
        """

        # Echo back information about what was posted in the form 
        for field in form.keys():
            """
            Para manejar archivos

            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write('\tUploaded %s (%d bytes)\n' % (field, file_len))
            else:
            """
            """mostramos los datos enviados por post"""
            """
            self.wfile.write('\t%s=%s\n' % (field, form[field].value))
            """

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

        if desktop == "lxde":
           if arch=="i386":
              taskLihuen="lihuen-lxde-base lihuen-lxde-desktop lihuen-base lihuen-i386"
           else:
              taskLihuen="lihuen-lxde-base lihuen-lxde-desktop lihuen-base lihuen-amd64"
        elif desktop=="cinnamon":
           if arch=="i386":
              taskLihuen="lihuen-lxde-base lihuen-cinnamon-desktop lihuen-base lihuen-i386"
           else:
              taskLihuen="lihuen-lxde-base lihuen-cinnamon-desktop lihuen-base lihuen-amd64"

        call(["cd ", "/usr/src/lihuen/Lihuen/testing"])

        comando="--architectures %s --binary-images iso-hybrid --bootstrapLihuen "user-setup" --chroot-filesystem %s --debian-installer live --debian-installer-gui %s --distribution %s --parent-distribution %s --parent-debian-installer-distribution %s --iso-application %s --lihuenChroot '/usr/src/lihuen/Lihuen/testing' --iso-volume %s  --parent-mirror-chroot %s --parent-mirror-binary %s --mirror-bootstrap %s --mirror-chroot %s --section-lihuen 'wheezy/experimental' --mirror-lihuen 'http://repo.lihuen.linti.unlp.edu.ar/lihuen' --archive-areas %s --archives-areas-lihuen 'main contrib non-free' --taskLihuen %s" % (arch,filesystem,di,distro,distro,distro,nombreiso,nombreiso,repoextra,repoextra,repoextra,area,taskLihuen)

        print comando

        call(["lb config", "--architectures arch --binary-images iso-hybrid --bootstrapLihuen "user-setup" --chroot-filesystem filesystem --debian-installer live --debian-installer-gui di --distribution distro --parent-distribution distro --parent-debian-installer-distribution distro --iso-application nombre --lihuenChroot '/usr/src/lihuen/Lihuen/testing' --iso-volume nombreiso  --parent-mirror-chroot repoextra --parent-mirror-binary repoextra --mirror-bootstrap repoextra  --mirror-chroot repoextra --section-lihuen 'wheezy/experimental' --mirror-lihuen 'http://repo.lihuen.linti.unlp.edu.ar/lihuen' --archive-areas area --archives-areas-lihuen 'main contrib non-free' --taskLihuen taskLihuen"])

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
