%define _requires_exceptions perl(\\(Kernel::.*\\|Win32\\))
%define _provides_exceptions perl(Kernel::.*)

Name:		otrs
Version:	3.1.11
Release:	%mkrel 1
Summary:    	The Open Ticket Request System
License:    	GPLv3+
Group:      	Networking/Other
URL:        	http://www.otrs.com
Source:     	http://ftp.otrs.org/pub/otrs/otrs-%{version}.tar.bz2
Requires:	apache-mod_perl
Suggests:	procmail
BuildArch:  	noarch

%description
OTRS is the leading open-source Help Desk and IT Service Management (ITSM)
solution used by thousands of organizations worldwide, enabling transparency
and collaboration for service desk and customer support teams, including those
implementing ITIL Best Practices. OTRS Group offers consulting, support,
customization and hosting services.

%prep
%setup -q
rm -rf Kernel/cpan-lib

%build
find  -type f | xargs perl -pi -e "s|/opt|/var/www|g"
# copy config file
cp Kernel/Config.pm.dist Kernel/Config.pm
cd Kernel/Config/ && for foo in *.dist; do cp $foo `basename $foo .dist`; done && cd ../../
# copy all crontab dist files
for foo in var/cron/*.dist; do mv $foo var/cron/`basename $foo .dist`; done
# copy all .dist files
cp .procmailrc.dist .procmailrc
cp .fetchmailrc.dist .fetchmailrc
cp .mailfilter.dist .mailfilter

%install
rm -rf %{buildroot}

# set DESTROOT
export DESTROOT="/var/www/otrs"
install -d %{buildroot}%{_var}/www/otrs
cp -R . %{buildroot}%{_var}/www/otrs

install -d -m 755 %{buildroot}/%{_webconfdir}/webapps.d

cat > %{buildroot}/%{_webconfdir}/webapps.d/otrs.conf << EOF

# added for OTRS (http://otrs.org/)
#$Id: installation-and-basic-configuration.xml,v 1.24 2009/08/27 22:34:47 martin Exp $

# agent, admin and customer frontend
ScriptAlias /otrs/ "/var/www/otrs/bin/cgi-bin/"
Alias /otrs-web/ "/var/www/otrs/var/httpd/htdocs/"
# if mod_perl is used
<IfModule mod_perl.c>
  # load all otrs modules
  Perlrequire /var/www/otrs/scripts/apache2-perl-startup.pl
  # Apache::Reload - Reload Perl Modules when Changed on Disk
  PerlModule Apache2::Reload
  PerlInitHandler Apache2::Reload
  PerlModule Apache2::RequestRec

  # set mod_perl2 options
  <Location /otrs>
    # ErrorDocument 403 /otrs/customer.pl
    ErrorDocument 403 /otrs/index.pl
    SetHandler perl-script
    PerlResponseHandler ModPerl::Registry
    Options +ExecCGI
    #
    PerlOptions +ParseHeaders
    PerlOptions +SetupEnv
    Order allow,deny
    Allow from all
  </Location>
</IfModule>

# directory settings
<Directory "/var/www/otrs/bin/cgi-bin/">
  AllowOverride None
  Options +ExecCGI -Includes
  Order allow,deny
  Allow from all
</Directory>

<Directory "/var/www/otrs/var/httpd/htdocs/">
  AllowOverride None
  Order allow,deny
  Allow from all
</Directory>
# MaxRequestsPerChild (so no apache child will be to big!)
MaxRequestsPerChild 400
EOF

%pre
%_pre_useradd otrs %{_var}/www/otrs /bin/false

%preun
%{_var}/www/otrs/bin/Cron.sh stop otrs

%post
%{_var}/www/otrs/bin/otrs.SetPermissions.pl  --otrs-user=otrs --web-user=apache --otrs-group=otrs --web-group=apache %{_var}/www/otrs
cd %{_var}/www/otrs/var/cron
for foo in *.dist; do cp $foo `basename $foo .dist`; done
%{_var}/www/otrs/bin/Cron.sh start otrs

%postun
%_postun_userdel otrs
%_postun_groupdel otrs

%files
%doc doc/* doc/manual/* ARCHIVE CHANGES COPYING COPYING-Third-Party CREDITS
%doc INSTALL INSTALL.RedHat INSTALL.SuSE README README.database README.webserver 
%doc UPGRADING
%dir %{_var}/www/otrs/doc/
%{_var}/www/otrs/ARCHIVE 
%{_var}/www/otrs/CHANGES 
%{_var}/www/otrs/COPYING 
%{_var}/www/otrs/COPYING-Third-Party 
%{_var}/www/otrs/CREDITS
%dir %{_var}/www/otrs/Custom/
%{_var}/www/otrs/INSTALL 
%{_var}/www/otrs/INSTALL.RedHat 
%{_var}/www/otrs/INSTALL.SuSE 
%{_var}/www/otrs/README 
%{_var}/www/otrs/README.database 
%{_var}/www/otrs/README.webserver
%{_var}/www/otrs/UPGRADING
%dir %{_var}/www/otrs/var/fonts/
%{_var}/www/otrs/var/fonts/*
%{_var}/www/otrs/RELEASE
%config(noreplace) %{_webconfdir}/webapps.d/otrs.conf
%config(noreplace) %attr(0644,otrs,apache) %{_var}/www/otrs/Kernel/Config.pm
%config(noreplace) %{_var}/www/otrs/Kernel/Config/GenericAgent.pm
%config(noreplace) %{_var}/www/otrs/.procmailrc
%config(noreplace) %{_var}/www/otrs/.fetchmailrc
%config(noreplace) %{_var}/www/otrs/.mailfilter
%config(noreplace) %{_var}/www/otrs/Kernel/Output/HTML/Standard/*.dtl
#config(noreplace) %{_var}/www/otrs/Kernel/Output/HTML/Lite/*.dtl
%config(noreplace) %{_var}/www/otrs/Kernel/Language/*.pm
%config(noreplace) %{_var}/www/otrs/var/cron/*
%config(noreplace) %{_var}/www/otrs/var/logo-otrs.png

%attr(0775,otrs,apache) %dir %{_var}/www/otrs/
%{_var}/www/otrs/.procmailrc.dist
%{_var}/www/otrs/.fetchmailrc.dist
%{_var}/www/otrs/.mailfilter.dist
%dir %{_var}/www/otrs/Kernel/
%dir %{_var}/www/otrs/Kernel/Config/
%{_var}/www/otrs/Kernel/Config.pm.dist
%attr(0775,otrs,apache) %{_var}/www/otrs/Kernel/Config/Files/
%{_var}/www/otrs/Kernel/Config/GenericAgent.pm.dist
%{_var}/www/otrs/Kernel/Config/GenericAgent.pm.examples
%{_var}/www/otrs/Kernel/Config/Defaults.pm
%{_var}/www/otrs/Kernel/Language.pm
%dir %{_var}/www/otrs/Kernel/Language/
%{_var}/www/otrs/Kernel/Modules*
%dir %{_var}/www/otrs/Kernel/Output/
%dir %{_var}/www/otrs/Kernel/Output/HTML/
%dir %{_var}/www/otrs/Kernel/Output/HTML/Standard/
#dir %{_var}/www/otrs/Kernel/Output/HTML/Lite/
%{_var}/www/otrs/Kernel/Output/HTML/*.pm
%{_var}/www/otrs/Kernel/System*
%attr(0775,otrs,apache) %{_var}/www/otrs/bin*
%{_var}/www/otrs/scripts*
%dir %{_var}/www/otrs/var/
%dir %{_var}/www/otrs/var/packages/
%{_var}/www/otrs/var/packages/*.opm
%attr(0775,otrs,apache) %dir %{_var}/www/otrs/var/article/
%{_var}/www/otrs/var/httpd/
%attr(0775,otrs,apache) %dir %{_var}/www/otrs/var/log/
%attr(0775,otrs,apache) %dir %{_var}/www/otrs/var/sessions/
%attr(0775,otrs,apache) %dir %{_var}/www/otrs/var/spool/
%dir %{_var}/www/otrs/var/cron/
%attr(0775,otrs,apache) %dir %{_var}/www/otrs/var/tmp/
%attr(0775,otrs,apache) %dir %{_var}/www/otrs/var/stats/
%{_var}/www/otrs/var/stats/*.xml
%dir %{_var}/www/otrs/var/tmp/Cache
#dir %{_var}/www/otrs/var/pics/stats/

%{_var}/www/otrs/Custom/README
%{_var}/www/otrs/Kernel/GenericInterface/Debugger.pm
%{_var}/www/otrs/Kernel/GenericInterface/Event/Handler.pm
%{_var}/www/otrs/Kernel/GenericInterface/Invoker.pm
%{_var}/www/otrs/Kernel/GenericInterface/Invoker/Test/Test.pm
%{_var}/www/otrs/Kernel/GenericInterface/Invoker/Test/TestSimple.pm
%{_var}/www/otrs/Kernel/GenericInterface/Mapping.pm
%{_var}/www/otrs/Kernel/GenericInterface/Mapping/Simple.pm
%{_var}/www/otrs/Kernel/GenericInterface/Mapping/Test.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Common.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Session/Common.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Session/SessionCreate.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Test/Test.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Ticket/Common.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Ticket/TicketCreate.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Ticket/TicketGet.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Ticket/TicketSearch.pm
%{_var}/www/otrs/Kernel/GenericInterface/Operation/Ticket/TicketUpdate.pm
%{_var}/www/otrs/Kernel/GenericInterface/Provider.pm
%{_var}/www/otrs/Kernel/GenericInterface/Requester.pm
%{_var}/www/otrs/Kernel/GenericInterface/Transport.pm
%{_var}/www/otrs/Kernel/GenericInterface/Transport/HTTP/REST.pm
%{_var}/www/otrs/Kernel/GenericInterface/Transport/HTTP/SOAP.pm
%{_var}/www/otrs/Kernel/GenericInterface/Transport/HTTP/Test.pm
%{_var}/www/otrs/Kernel/Scheduler.pm
%{_var}/www/otrs/Kernel/Scheduler/TaskHandler.pm
%{_var}/www/otrs/Kernel/Scheduler/TaskHandler/GenericInterface.pm
%{_var}/www/otrs/Kernel/Scheduler/TaskHandler/Test.pm
%{_var}/www/otrs/doc/OTRSDatabaseDiagram.mwb
%{_var}/www/otrs/doc/OTRSDatabaseDiagram.png
%{_var}/www/otrs/doc/X-OTRS-Headers.txt
%{_var}/www/otrs/doc/manual/de/otrs_admin_book.pdf
%{_var}/www/otrs/doc/manual/en/otrs_admin_book.pdf
%{_var}/www/otrs/doc/sample_mails/Readme.txt
%{_var}/www/otrs/doc/sample_mails/test-email-1.box
%{_var}/www/otrs/doc/sample_mails/test-email-10-ks_c_5601-1987.box
%{_var}/www/otrs/doc/sample_mails/test-email-2.box
%{_var}/www/otrs/doc/sample_mails/test-email-3.box
%{_var}/www/otrs/doc/sample_mails/test-email-4-html.box
%{_var}/www/otrs/doc/sample_mails/test-email-5-iso-8859-1.box
%{_var}/www/otrs/doc/sample_mails/test-email-6-euro-utf-8.box
%{_var}/www/otrs/doc/sample_mails/test-email-7-euro-iso-8859-15.box
%{_var}/www/otrs/doc/sample_mails/test-email-8-bulgarian-cp1251.box
%{_var}/www/otrs/doc/sample_mails/test-email-9-html-multicharset.box

%changelog

