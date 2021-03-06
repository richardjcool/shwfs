/*
 * DO NOT EDIT THIS FILE - it is generated by Glade.
 */

#ifdef HAVE_CONFIG_H
#  include <config.h>
#endif

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

#include <gdk/gdkkeysyms.h>
#include <gtk/gtk.h>

#include "callbacks.h"
#include "interface.h"
#include "support.h"

#define GLADE_HOOKUP_OBJECT(component,widget,name) \
  g_object_set_data_full (G_OBJECT (component), name, \
    gtk_widget_ref (widget), (GDestroyNotify) gtk_widget_unref)

#define GLADE_HOOKUP_OBJECT_NO_REF(component,widget,name) \
  g_object_set_data (G_OBJECT (component), name, widget)

GtkWidget*
create_MainWindow (void)
{
  GtkWidget *MainWindow;
  GtkWidget *vbox1;
  GtkWidget *menubar1;
  GtkWidget *menuitem1;
  GtkWidget *menuitem1_menu;
  GtkWidget *quit1;
  GtkWidget *menuitem4;
  GtkWidget *menuitem4_menu;
  GtkWidget *about1;
  GtkWidget *table1;
  GtkWidget *label1;
  GtkWidget *label2;
  GtkWidget *FindTel;
  GtkWidget *FindHere;
  GtkWidget *RA;
  GtkWidget *Dec;
  GtkWidget *label3;
  GtkObject *FlipVal_adj;
  GtkWidget *FlipVal;
  GtkWidget *Flip;
  GtkWidget *label4;
  GtkWidget *mag;
  GtkWidget *label5;
  GtkWidget *inner;
  GtkWidget *outer;
  GtkWidget *scrolledwindow1;
  GtkWidget *OutputTree;
  GtkWidget *cb_stoprefreshing;
  GtkWidget *GoOnAxis;
  GtkWidget *GoOffAxis;
  GtkWidget *Return;
  GtkWidget *Status;
  GtkAccelGroup *accel_group;

  accel_group = gtk_accel_group_new ();

  MainWindow = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_window_set_title (GTK_WINDOW (MainWindow), _("Continuous WFS Catalog GUI"));
  gtk_window_set_default_size (GTK_WINDOW (MainWindow), 700, -1);

  vbox1 = gtk_vbox_new (FALSE, 0);
  gtk_widget_show (vbox1);
  gtk_container_add (GTK_CONTAINER (MainWindow), vbox1);

  menubar1 = gtk_menu_bar_new ();
  gtk_widget_show (menubar1);
  gtk_box_pack_start (GTK_BOX (vbox1), menubar1, FALSE, FALSE, 0);

  menuitem1 = gtk_menu_item_new_with_mnemonic (_("_File"));
  gtk_widget_show (menuitem1);
  gtk_container_add (GTK_CONTAINER (menubar1), menuitem1);

  menuitem1_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (menuitem1), menuitem1_menu);

  quit1 = gtk_image_menu_item_new_from_stock ("gtk-quit", accel_group);
  gtk_widget_show (quit1);
  gtk_container_add (GTK_CONTAINER (menuitem1_menu), quit1);

  menuitem4 = gtk_menu_item_new_with_mnemonic (_("_Help"));
  gtk_widget_show (menuitem4);
  gtk_container_add (GTK_CONTAINER (menubar1), menuitem4);

  menuitem4_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (menuitem4), menuitem4_menu);

  about1 = gtk_menu_item_new_with_mnemonic (_("_About"));
  gtk_widget_show (about1);
  gtk_container_add (GTK_CONTAINER (menuitem4_menu), about1);

  table1 = gtk_table_new (4, 5, FALSE);
  gtk_widget_show (table1);
  gtk_box_pack_start (GTK_BOX (vbox1), table1, FALSE, TRUE, 0);
  gtk_container_set_border_width (GTK_CONTAINER (table1), 10);
  gtk_table_set_row_spacings (GTK_TABLE (table1), 10);
  gtk_table_set_col_spacings (GTK_TABLE (table1), 5);

  label1 = gtk_label_new (_("RA:"));
  gtk_widget_show (label1);
  gtk_table_attach (GTK_TABLE (table1), label1, 0, 1, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label1), 1, 0.5);

  label2 = gtk_label_new (_("Dec:"));
  gtk_widget_show (label2);
  gtk_table_attach (GTK_TABLE (table1), label2, 0, 1, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label2), 1, 0.5);

  FindTel = gtk_button_new_with_mnemonic (_("Find at Current Telescope Catalog Position"));
  gtk_widget_show (FindTel);
  gtk_table_attach (GTK_TABLE (table1), FindTel, 2, 5, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  FindHere = gtk_button_new_with_mnemonic (_("Find at Specified Coordinates"));
  gtk_widget_show (FindHere);
  gtk_table_attach (GTK_TABLE (table1), FindHere, 2, 5, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  RA = gtk_entry_new ();
  gtk_widget_show (RA);
  gtk_table_attach (GTK_TABLE (table1), RA, 1, 2, 0, 1,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 10, 0);
  GTK_WIDGET_UNSET_FLAGS (RA, GTK_CAN_FOCUS);
  gtk_entry_set_max_length (GTK_ENTRY (RA), 15);

  Dec = gtk_entry_new ();
  gtk_widget_show (Dec);
  gtk_table_attach (GTK_TABLE (table1), Dec, 1, 2, 1, 2,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 10, 0);
  gtk_entry_set_max_length (GTK_ENTRY (Dec), 15);

  label3 = gtk_label_new (_("Flip:"));
  gtk_widget_show (label3);
  gtk_table_attach (GTK_TABLE (table1), label3, 0, 1, 3, 4,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label3), 0, 0.5);

  FlipVal_adj = gtk_adjustment_new (180, -180, 180, 180, 180, 0);
  FlipVal = gtk_spin_button_new (GTK_ADJUSTMENT (FlipVal_adj), 1, 0);
  gtk_widget_show (FlipVal);
  gtk_table_attach (GTK_TABLE (table1), FlipVal, 1, 2, 3, 4,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 10, 0);

  Flip = gtk_button_new_with_mnemonic (_("Set Flip"));
  gtk_widget_show (Flip);
  gtk_table_attach (GTK_TABLE (table1), Flip, 2, 5, 3, 4,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  label4 = gtk_label_new (_("limiting magnitude"));
  gtk_widget_show (label4);
  gtk_table_attach (GTK_TABLE (table1), label4, 0, 1, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label4), 0, 0.5);

  mag = gtk_entry_new ();
  gtk_widget_show (mag);
  gtk_table_attach (GTK_TABLE (table1), mag, 1, 2, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_entry_set_text (GTK_ENTRY (mag), _("14"));
  gtk_entry_set_invisible_char (GTK_ENTRY (mag), 8226);

  label5 = gtk_label_new (_("radii in/out (arcmin)"));
  gtk_widget_show (label5);
  gtk_table_attach (GTK_TABLE (table1), label5, 2, 3, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label5), 0, 0.5);

  inner = gtk_entry_new ();
  gtk_widget_show (inner);
  gtk_table_attach (GTK_TABLE (table1), inner, 3, 4, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_entry_set_text (GTK_ENTRY (inner), _("20"));
  gtk_entry_set_invisible_char (GTK_ENTRY (inner), 8226);

  outer = gtk_entry_new ();
  gtk_widget_show (outer);
  gtk_table_attach (GTK_TABLE (table1), outer, 4, 5, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_entry_set_text (GTK_ENTRY (outer), _("30"));
  gtk_entry_set_invisible_char (GTK_ENTRY (outer), 8226);

  scrolledwindow1 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow1);
  gtk_box_pack_start (GTK_BOX (vbox1), scrolledwindow1, TRUE, TRUE, 0);

  OutputTree = gtk_tree_view_new ();
  gtk_widget_show (OutputTree);
  gtk_container_add (GTK_CONTAINER (scrolledwindow1), OutputTree);
  gtk_widget_set_size_request (OutputTree, 126, 200);
  gtk_tree_view_set_reorderable (GTK_TREE_VIEW (OutputTree), TRUE);

  cb_stoprefreshing = gtk_check_button_new_with_mnemonic (_("Stop Auto-Refreshing"));
  gtk_widget_show (cb_stoprefreshing);
  gtk_box_pack_start (GTK_BOX (vbox1), cb_stoprefreshing, FALSE, FALSE, 0);

  GoOnAxis = gtk_button_new_with_mnemonic (_("Go to Selected Star On Axis"));
  gtk_widget_show (GoOnAxis);
  gtk_box_pack_start (GTK_BOX (vbox1), GoOnAxis, FALSE, FALSE, 0);
  gtk_container_set_border_width (GTK_CONTAINER (GoOnAxis), 5);

  GoOffAxis = gtk_button_new_with_mnemonic (_("Go to Selected Star Off Axis"));
  gtk_widget_show (GoOffAxis);
  gtk_box_pack_start (GTK_BOX (vbox1), GoOffAxis, FALSE, FALSE, 0);
  gtk_container_set_border_width (GTK_CONTAINER (GoOffAxis), 5);

  Return = gtk_button_new_with_mnemonic (_("Stow WFS"));
  gtk_widget_show (Return);
  gtk_box_pack_start (GTK_BOX (vbox1), Return, FALSE, FALSE, 0);
  gtk_container_set_border_width (GTK_CONTAINER (Return), 5);

  Status = gtk_statusbar_new ();
  gtk_widget_show (Status);
  gtk_box_pack_start (GTK_BOX (vbox1), Status, FALSE, FALSE, 0);

  g_signal_connect ((gpointer) MainWindow, "destroy",
                    G_CALLBACK (on_MainWindow_destroy),
                    NULL);
  g_signal_connect ((gpointer) quit1, "activate",
                    G_CALLBACK (on_quit1_activate),
                    NULL);
  g_signal_connect ((gpointer) about1, "activate",
                    G_CALLBACK (on_about1_activate),
                    NULL);
  g_signal_connect ((gpointer) FindTel, "clicked",
                    G_CALLBACK (on_FindTel_clicked),
                    NULL);
  g_signal_connect ((gpointer) FindHere, "clicked",
                    G_CALLBACK (on_FindHere_clicked),
                    NULL);
  g_signal_connect ((gpointer) Flip, "clicked",
                    G_CALLBACK (on_Flip_clicked),
                    NULL);
  g_signal_connect ((gpointer) cb_stoprefreshing, "toggled",
                    G_CALLBACK (on_cb_stoprefreshing_toggled),
                    NULL);
  g_signal_connect ((gpointer) GoOnAxis, "clicked",
                    G_CALLBACK (on_GoOnAxis_clicked),
                    NULL);
  g_signal_connect ((gpointer) GoOffAxis, "clicked",
                    G_CALLBACK (on_GoOffAxis_clicked),
                    NULL);
  g_signal_connect ((gpointer) Return, "clicked",
                    G_CALLBACK (on_Return_clicked),
                    NULL);

  /* Store pointers to all widgets, for use by lookup_widget(). */
  GLADE_HOOKUP_OBJECT_NO_REF (MainWindow, MainWindow, "MainWindow");
  GLADE_HOOKUP_OBJECT (MainWindow, vbox1, "vbox1");
  GLADE_HOOKUP_OBJECT (MainWindow, menubar1, "menubar1");
  GLADE_HOOKUP_OBJECT (MainWindow, menuitem1, "menuitem1");
  GLADE_HOOKUP_OBJECT (MainWindow, menuitem1_menu, "menuitem1_menu");
  GLADE_HOOKUP_OBJECT (MainWindow, quit1, "quit1");
  GLADE_HOOKUP_OBJECT (MainWindow, menuitem4, "menuitem4");
  GLADE_HOOKUP_OBJECT (MainWindow, menuitem4_menu, "menuitem4_menu");
  GLADE_HOOKUP_OBJECT (MainWindow, about1, "about1");
  GLADE_HOOKUP_OBJECT (MainWindow, table1, "table1");
  GLADE_HOOKUP_OBJECT (MainWindow, label1, "label1");
  GLADE_HOOKUP_OBJECT (MainWindow, label2, "label2");
  GLADE_HOOKUP_OBJECT (MainWindow, FindTel, "FindTel");
  GLADE_HOOKUP_OBJECT (MainWindow, FindHere, "FindHere");
  GLADE_HOOKUP_OBJECT (MainWindow, RA, "RA");
  GLADE_HOOKUP_OBJECT (MainWindow, Dec, "Dec");
  GLADE_HOOKUP_OBJECT (MainWindow, label3, "label3");
  GLADE_HOOKUP_OBJECT (MainWindow, FlipVal, "FlipVal");
  GLADE_HOOKUP_OBJECT (MainWindow, Flip, "Flip");
  GLADE_HOOKUP_OBJECT (MainWindow, label4, "label4");
  GLADE_HOOKUP_OBJECT (MainWindow, mag, "mag");
  GLADE_HOOKUP_OBJECT (MainWindow, label5, "label5");
  GLADE_HOOKUP_OBJECT (MainWindow, inner, "inner");
  GLADE_HOOKUP_OBJECT (MainWindow, outer, "outer");
  GLADE_HOOKUP_OBJECT (MainWindow, scrolledwindow1, "scrolledwindow1");
  GLADE_HOOKUP_OBJECT (MainWindow, OutputTree, "OutputTree");
  GLADE_HOOKUP_OBJECT (MainWindow, cb_stoprefreshing, "cb_stoprefreshing");
  GLADE_HOOKUP_OBJECT (MainWindow, GoOnAxis, "GoOnAxis");
  GLADE_HOOKUP_OBJECT (MainWindow, GoOffAxis, "GoOffAxis");
  GLADE_HOOKUP_OBJECT (MainWindow, Return, "Return");
  GLADE_HOOKUP_OBJECT (MainWindow, Status, "Status");

  gtk_window_add_accel_group (GTK_WINDOW (MainWindow), accel_group);

  return MainWindow;
}

