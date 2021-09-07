#
# OMNeT++/OMNEST Makefile for $(LIB_PREFIX)veins_libairmobisim
#
# This file was generated with the command:
#  opp_makemake -f --deep --no-deep-includes --make-so -I . -o veins_libairmobisim -O out
#

# Name of target to be created (-o option)
TARGET = $(LIB_PREFIX)veins_libairmobisim$(D)$(SHARED_LIB_SUFFIX)
TARGET_DIR = .

# C++ include paths (with -I)
INCLUDE_PATH = -I.

# Additional object and library files to link with
EXTRA_OBJS =

# Additional libraries (-L, -l options)
LIBS =

# Output directory
PROJECT_OUTPUT_DIR = ../out
PROJECTRELATIVE_PATH = src
O = $(PROJECT_OUTPUT_DIR)/$(CONFIGNAME)/$(PROJECTRELATIVE_PATH)

# Object files for local .cc, .msg and .sm files
OBJS = $O/proto/airmobisim.grpc.pb.o $O/proto/airmobisim.pb.o $O/veins_libairmobisim/DroCIManager.o

# Message files
MSGFILES =

# SM files
SMFILES =

#------------------------------------------------------------------------------

# Pull in OMNeT++ configuration (Makefile.inc)

ifneq ("$(OMNETPP_CONFIGFILE)","")
CONFIGFILE = $(OMNETPP_CONFIGFILE)
else
ifneq ("$(OMNETPP_ROOT)","")
CONFIGFILE = $(OMNETPP_ROOT)/Makefile.inc
else
CONFIGFILE = $(shell opp_configfilepath)
endif
endif

ifeq ("$(wildcard $(CONFIGFILE))","")
$(error Config file '$(CONFIGFILE)' does not exist -- add the OMNeT++ bin directory to the path so that opp_configfilepath can be found, or set the OMNETPP_CONFIGFILE variable to point to Makefile.inc)
endif

include $(CONFIGFILE)

# Simulation kernel and user interface libraries
OMNETPP_LIBS = -loppenvir$D $(KERNEL_LIBS) $(SYS_LIBS)

COPTS = $(CFLAGS) $(IMPORT_DEFINES)  $(INCLUDE_PATH) -I$(OMNETPP_INCL_DIR)
MSGCOPTS = $(INCLUDE_PATH)
SMCOPTS =

# we want to recompile everything if COPTS changes,
# so we store COPTS into $COPTS_FILE and have object
# files depend on it (except when "make depend" was called)
COPTS_FILE = $O/.last-copts
ifneq ("$(COPTS)","$(shell cat $(COPTS_FILE) 2>/dev/null || echo '')")
$(shell $(MKPATH) "$O" && echo "$(COPTS)" >$(COPTS_FILE))
endif

#------------------------------------------------------------------------------
# User-supplied makefile fragment(s)
# >>>
# inserted from file 'makefrag':

#
# Copyright (C) 2017 Rudolf Hornig <rudi@omnetpp.org>
# Copyright (C) 2018-2020 Christoph Sommer <sommer@cms-labs.org>
#
# Documentation for these modules is at http://veins.car2x.org/
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

#
# on windows, special care is needed for linking
# adapted from INET Framework (inet-4.2.1) makefrag
#
ifeq ($(PLATFORM),win32.x86_64)
  #
  # on windows we have to link with the ws2_32 (winsock2) library as it is no longer added
  # to the omnetpp system libraries by default (as of OMNeT++ 5.1)
  #
  LIBS += -lws2_32
  ENABLE_AUTO_IMPORT=-Wl,--enable-auto-import
  LDFLAGS := $(filter-out $(ENABLE_AUTO_IMPORT), $(LDFLAGS))

  # FIX for clang not exporting typeinfo and other thunks on Windows
  ifeq ($(CC),clang)
    DEFFILE = $O/typeinfo.def
    LDFLAGS += $(DEFFILE)

.PHONY: all

all:

$(DEFFILE): $(OBJS)  $(wildcard $(EXTRA_OBJS)) Makefile $(CONFIGFILE)
	$(Q)$(DLLTOOL) --export-all-symbols --kill-at --output-def $O/all.def $(OBJS) $(EXTRA_OBJS)
	$(Q)grep -E '( *_ZTI)|( *_ZThn)|( *_ZTv0)|EXPORTS' $O/all.def | sed 's/ @.*//' >$(DEFFILE)

$O/$(TARGET): $(DEFFILE)

  endif
endif

#
# Use the new message compiler introduced in OMNeT++ 5.3
#
MSGC:=$(MSGC) --msg6

# pull in fallback values from Makefile.inc.default
include Makefile.inc.default

# compile/link with grpc
LIBS += -lgrpc++
LDFLAGS += -Wl,-rpath,$(abspath $(GRPC_PLUGIN_LIBRARY))
INCLUDE_PATH += -I$(GRPC_PLUGIN_INCLUDE)

#CFLAGS += `pkg-config --cflags protobuf grpc`
#LIBS += `pkg-config --libs protobuf grpc++ grpc` -lgrpc++_reflection -ldl
#INCLUDE_PATH += -I/usr/local/include -I/usr/local/include/absl

# <<<
#------------------------------------------------------------------------------

# Main target
all: $(TARGET_DIR)/$(TARGET)

$(TARGET_DIR)/% :: $O/%
	@mkdir -p $(TARGET_DIR)
	$(Q)$(LN) $< $@
ifeq ($(TOOLCHAIN_NAME),clangc2)
	$(Q)-$(LN) $(<:%.dll=%.lib) $(@:%.dll=%.lib)
endif

$O/$(TARGET): $(OBJS)  $(wildcard $(EXTRA_OBJS)) Makefile $(CONFIGFILE)
	@$(MKPATH) $O
	@echo Creating shared library: $@
	$(Q)$(SHLIB_LD) -o $O/$(TARGET) $(OBJS) $(EXTRA_OBJS) $(AS_NEEDED_OFF) $(WHOLE_ARCHIVE_ON) $(LIBS) $(WHOLE_ARCHIVE_OFF) $(OMNETPP_LIBS) $(LDFLAGS)
	$(Q)$(SHLIB_POSTPROCESS) $O/$(TARGET)

.PHONY: all clean cleanall depend msgheaders smheaders

.SUFFIXES: .cc

$O/%.o: %.cc $(COPTS_FILE) | msgheaders smheaders
	@$(MKPATH) $(dir $@)
	$(qecho) "$<"
	$(Q)$(CXX) -c $(CXXFLAGS) $(COPTS) -o $@ $<

%_m.cc %_m.h: %.msg
	$(qecho) MSGC: $<
	$(Q)$(MSGC) -s _m.cc -MD -MP -MF $O/$(basename $<)_m.h.d $(MSGCOPTS) $?

%_sm.cc %_sm.h: %.sm
	$(qecho) SMC: $<
	$(Q)$(SMC) -c++ -suffix cc $(SMCOPTS) $?

msgheaders: $(MSGFILES:.msg=_m.h)

smheaders: $(SMFILES:.sm=_sm.h)

clean:
	$(qecho) Cleaning $(TARGET)
	$(Q)-rm -rf $O
	$(Q)-rm -f $(TARGET_DIR)/$(TARGET)
	$(Q)-rm -f $(TARGET_DIR)/$(TARGET:%.dll=%.lib)
	$(Q)-rm -f $(call opp_rwildcard, . , *_m.cc *_m.h *_sm.cc *_sm.h)

cleanall:
	$(Q)$(MAKE) -s clean MODE=release
	$(Q)$(MAKE) -s clean MODE=debug
	$(Q)-rm -rf $(PROJECT_OUTPUT_DIR)

# include all dependencies
-include $(OBJS:%=%.d) $(MSGFILES:%.msg=$O/%_m.h.d)
