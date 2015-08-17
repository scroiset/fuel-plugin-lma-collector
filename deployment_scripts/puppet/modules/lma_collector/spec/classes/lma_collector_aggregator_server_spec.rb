#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
require 'spec_helper'

describe 'lma_collector::aggregator::server' do
    let(:facts) do
        {:kernel => 'Linux', :operatingsystem => 'Ubuntu',
         :osfamily => 'Debian'}
    end

    describe 'with defaults' do
        it { is_expected.to contain_heka__input__tcp('aggregator') }
        it { is_expected.not_to contain_heka__input__http_listen('check-http') }
    end

    describe 'with http_check_port = 3000' do
        let(:params) do
            {:http_check_port => 3000}
        end
        it { is_expected.to contain_heka__input__tcp('aggregator') }
        it { is_expected.to contain_heka__input__httplisten('http-check').with_port(3000) }
    end
end
