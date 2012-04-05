%define _exclude_files_from_autoprov %{_var}/www/otrs/Kernel/cpan-lib
%define _requires_exceptions perl.Kernel\\|perl.HTML..Safe.|perl.Algorithm|perl.Apache|perl.Authen|perl.Crypt|perl.Date|perl.File|perl.IO|perl.MIME|perl.Mail|perl.Net|perl.Text|perl.XML
%define _provides_exceptions %_requires_exceptions
Name:		otrs
Version:	3.1.3
Release:	%mkrel 1
Summary:    	The Open Ticket Request System
License:    	GPLv3+
Group:      	Networking/Other
URL:        	http://www.otrs.com
Source0:     	http://ftp.otrs.org/pub/otrs/otrs-%{version}.tar.bz2
# Disable Auto requires/provides as it conflicts with a lot of perl rpms
AutoReqProv: 1
Requires:	apache-mod_perl
Requires:	perl-CGI
Requires:	perl-DBI
Requires:	perl-DBD-mysql
Requires:	perl-Digest-MD5
Requires:	perl-MIME-Base64
Requires:	perl-MIME-tools
Requires:	perl-Net-DNS
Requires:	perl-Authen-SASL
Suggests:	perl-GDTextUtil
Suggests:	perl-GDGraph 
Suggests:	perl-PDF-API2
Requires:	perl-Compress-Raw-Zlib
Requires:	mysql
Requires:	perl-Date-Calc
Suggests:	perl-IO-Socket-SSL
Suggests:	perl-Encode-HanExtra
Suggests:	perl-Net-IMAP-Simple-SSL
Suggests:	perl-ldap
Suggests:	perl-SOAP-Lite
Suggests:	perl-Apache-DBI
Suggests:	perl-Net-SMTP-SSL
Suggests:	perl-Authen-Radius
Suggests:	procmail
Requires:	perl(Algorithm::Diff)
Requires:	perl(Apache::DBI)
Requires:	perl(Apache2::Reload)
Requires:	perl(Authen::SASL)
Requires:	perl(CGI)
Requires:	perl(Crypt::PasswdMD5)
Requires:	perl(Date::Pcalc)
Requires:	perl(Digest::SHA::PurePerl)
Requires:	perl(File::Temp)
Requires:	perl-IO-stringy
Requires:	perl(JSON::PP)
Requires:	perl(CSS)
Requires:	perl(JavaScript)
Requires:	perl-MIME-tools
Requires:	perl-MailTools
Requires:	perl(Net::IMAP::Simple)
Requires:	perl(Net::SMTP::SSL)
Requires:	perl(Text::CSV)
Requires:	perl(Text::Diff)
Requires:	perl(XML::FeedPP)
Requires:	perl(XML::Parser::Lite)

BuildRoot:  %{_tmppath}/%{name}-%{version}
BuildArch:  	noarch

%description
The Open Ticket Request System (http://otrs.org/) is a web based ticket system

Feedback: feedback@otrs.org

  OTRS is an Open source Ticket Request System with many features to manage
  customer telephone calls and e-mails. It is distributed under the GNU
  AFFERO General Public License (AGPL) and tested on Linux, Solaris, AIX,
  FreeBSD, OpenBSD and Mac OS 10.x. Do you receive many e-mails and want to
  answer them with a team of agents? You're going to love the OTRS!

  Feature list:

   Web-Interface:
    - Agent web interface for viewing and working on all customer requests
    - Admin web interface for changing system things
    - Customer web interface for viewing and sending infos to the agents
    - Webinterface with themes support
    - Multi language support (Brazilian Portuguese, Bulgarian, Dutch, English,
       Finnish, French, German, Italian and Spanish)
    - customize the output templates (dtl) release independently
    - Webinterface with attachment support
    - easy and logical to use

   Email-Interface:
    - PGP support
    - SMIME support
    - MIME support (attachments)
    - dispatching of incoming email via email 
	addess or x-header
    - autoresponders for customers by incoming emails 
	(per queue)
    - email-notification to the agent by new tickets, 
	follow ups or lock timeouts

   Ticket:
    - custom queue view and queue view of all requests
    - Ticket locking
    - Ticket replies (standard responses)
    - Ticket autoresponders per queue
    - Ticket history, evolution of ticket status and actions taken on ticket
    - abaility to add notes (with different note types) to a ticket
    - Ticket zoom feature
    - Tickets can be bounced or forwarded to other email addresses
    - Ticket can be moved to a different queue (this is helpful if emails are
       for a specific subject)
    - Ticket priority
    - Ticket time accounting
    - Ticket merge feature
    - Ticket ACL support
    - content Fulltext search

   System:
    - creation and configuration of user accounts, and groups
    - creation of standard responses
    - Signature configuration per queue
    - Salutation configuration per queue
    - email-notification of administrators
    - email-notification sent to problem reporter (by create, locked, deleted,
       moved and closed)
    - submitting update-info (via email or webinterface).
    - deadlines for trouble tickets
    - ASP (activ service providing) support
    - TicketHook free setable like 'Call#', 'MyTicket#', 'Request#' or 
	'Ticket#'
    - Ticket number format free setable
    - different levels of permissions/access-rights.
    - central database, Support of different SQL databases (e. g. MySQL, 
	PostgeSQL, ...)
    - user authentication agains database or ldap directory
    - easy to develope you own addon's (OTRS API)
    - easy to write different frontends (e. g. X11, console, ...)
    - own package manager (e. g. for application modules like webmail, 
	calendar or
       filemanager)
    - a fast and useful application

%prep
%setup

%build
pushd Kernel/cpan-lib/
rm -rf Algorithm/ Apache Apache2 Authen/ CGI* Crypt/ Date/ Digest/ File/ IO/ JSON*  CSS/ JavaScript/ MIME/ Mail/ Net/IMAP/ Net/SMTP/ Text/ XML/
popd

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
%if "%{distribution}" == "Mandriva Linux"
	%if %mdkversion < 201010
	%_post_webapp
	%endif
%endif

%postun
%_postun_userdel otrs
%_postun_groupdel otrs

%if "%{distribution}" == "Mandriva Linux"
	%if %mdkversion < 201010
	%_postun_webapp
	%endif
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,root)
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

%{_var}/www/otrs/Kernel/cpan-lib*

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

