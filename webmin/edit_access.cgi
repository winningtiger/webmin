#!/usr/local/bin/perl
# edit_access.cgi
# Display IP access control form

require './webmin-lib.pl';
&ui_print_header(undef, $text{'access_title'}, "");
&get_miniserv_config(\%miniserv);

print $text{'access_desc'},"<p>\n";

print &ui_form_start("change_access.cgi", "post");
print &ui_table_start($text{'access_header'}, undef, 2, [ "width=30%" ]);

$access = $miniserv{"allow"} ? 1 : $miniserv{"deny"} ? 2 : 0;
@list = $access == 1 ? split(/\s+/, $miniserv{"allow"}) :
	$access == 2 ? split(/\s+/, $miniserv{"deny"}) : ( );
$idx = &indexof("LOCAL", @list);
splice(@list, $idx, 1) if ($idx >= 0);
print &ui_table_row($text{'access_ip'},
	&ui_radio("access", $access,
	 	  [ [ 0, $text{'access_all'} ],
	 	    [ 1, $text{'access_allow'} ],
	 	    [ 2, $text{'access_deny'} ] ])."<br>\n".
	&ui_textarea("ip", join("\n", @list), 6, 30)."<br>\n".
	&ui_checkbox("local", 1, $text{'access_local'}, $idx >= 0));

print &ui_table_row($text{'access_always'},
	&ui_yesno_radio("alwaysresolve", int($miniserv{'alwaysresolve'})));

print &ui_table_row(&hlink($text{'access_trust'}, "access_trust"),
	&ui_yesno_radio("trust", int($miniserv{'trust_real_ip'})));

print &ui_table_row(&hlink($text{'access_trust_ssl'}, "access_trust_ssl"),
	&ui_radio("trust_ssl", $miniserv{'no_trust_ssl'} ? 1 : 0,
		  [ [ 0, $text{'access_trust_ssl_yes'} ],
		    [ 1, $text{'no'} ] ]));

eval "use Authen::Libwrap qw(hosts_ctl STRING_UNKNOWN)";
if (!$@) {
	print &ui_table_row($text{'access_libwrap'},
		&ui_yesno_radio("libwrap", int($miniserv{'libwrap'})));
	}

print &ui_table_end();
print &ui_form_end([ [ "save", $text{'save'} ] ]);

&ui_print_footer("", $text{'index_return'});

