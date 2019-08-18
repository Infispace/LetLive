LetLive Code Documentation
==========================

- The documentation is generated using
[Sphinx](http://www.sphinx-doc.org)

- To generate the module documentation use
[sphinx-apidoc](http://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)

```console
foo@bar:~$ sphinx-apidoc -M -o source/modules ..
```

- Build the docs files using make

```console
foo@bar:~$ make html
```
