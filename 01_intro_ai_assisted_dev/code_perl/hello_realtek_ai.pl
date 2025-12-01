#!/usr/bin/perl
use strict;
use warnings;

sub greet {
    my ($name) = @_;
    $name //= "Engineer";  # 使用預設值 "Engineer" 如果沒有提供名稱
    return "Hello, $name from Realtek!";
}

sub validate_name {
    my ($name) = @_;
    unless (defined $name && ref $name eq '') {
        die "Name must be a string";
    }
    return $name;
}

sub main {
    print "請輸入你的名字：";
    my $name = validate_name(<STDIN>);
    print greet($name), "\n";
}

main;